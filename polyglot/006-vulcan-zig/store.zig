const std = @import("std");

pub const max_snapshot = 1024 * 1024;
pub const Entry = struct { key: []const u8, value: []const u8 };

pub fn validate(key: []const u8, value: []const u8) !void {
    if (key.len == 0 or key.len > 64 or value.len > 4096) return error.InvalidEntry;
    for (key) |c| {
        if (!std.ascii.isAlphanumeric(c) and c != '_' and c != '-') return error.InvalidKey;
    }
    for (value) |c| {
        if (c < 32 or c == 127) return error.InvalidValue;
    }
}

pub fn parse(line: []const u8) !Entry {
    const sep = std.mem.indexOfScalar(u8, line, '\t') orelse return error.InvalidRecord;
    const entry: Entry = .{ .key = line[0..sep], .value = line[sep + 1 ..] };
    try validate(entry.key, entry.value);
    return entry;
}

pub fn load(allocator: std.mem.Allocator, path: []const u8) ![]const u8 {
    const data = std.fs.cwd().readFileAlloc(allocator, path, max_snapshot) catch |err| switch (err) {
        error.FileNotFound => return allocator.alloc(u8, 0),
        else => return err,
    };
    errdefer allocator.free(data);
    if (data.len > 0 and data[data.len - 1] != '\n') return error.TruncatedSnapshot;
    var lines = std.mem.tokenizeScalar(u8, data, '\n');
    while (lines.next()) |line| _ = try parse(line);
    return data;
}

pub fn get(data: []const u8, key: []const u8) !?[]const u8 {
    try validate(key, "");
    var lines = std.mem.tokenizeScalar(u8, data, '\n');
    var found: ?[]const u8 = null;
    while (lines.next()) |line| {
        const entry = try parse(line);
        if (std.mem.eql(u8, entry.key, key)) found = entry.value;
    }
    return found;
}

pub fn save(path: []const u8, data: []const u8, key: []const u8, value: ?[]const u8) !void {
    try validate(key, value orelse "");
    var atomic = try std.fs.cwd().atomicFile(path, .{});
    defer atomic.deinit();
    var written: usize = 0;
    var lines = std.mem.tokenizeScalar(u8, data, '\n');
    while (lines.next()) |line| {
        const entry = try parse(line);
        if (std.mem.eql(u8, entry.key, key)) continue;
        try atomic.file.writeAll(line);
        try atomic.file.writeAll("\n");
        written += line.len + 1;
    }
    if (value) |content| {
        if (written + key.len + content.len + 2 > max_snapshot) return error.SnapshotFull;
        try atomic.file.writeAll(key);
        try atomic.file.writeAll("\t");
        try atomic.file.writeAll(content);
        try atomic.file.writeAll("\n");
    }
    try atomic.file.sync();
    try atomic.finish();
}

test "snapshot survives updates and deletion" {
    var tmp = std.testing.tmpDir(.{});
    defer tmp.cleanup();
    const allocator = std.testing.allocator;
    const dir = try tmp.dir.realpathAlloc(allocator, ".");
    defer allocator.free(dir);
    const path = try std.fs.path.join(allocator, &.{ dir, "data" });
    defer allocator.free(path);
    try save(path, "", "a", "first");
    const first = try load(allocator, path);
    defer allocator.free(first);
    try std.testing.expectEqualStrings("first", (try get(first, "a")).?);
    try save(path, first, "a", "second");
    const second = try load(allocator, path);
    defer allocator.free(second);
    try std.testing.expectEqualStrings("second", (try get(second, "a")).?);
    try save(path, second, "a", null);
    const third = try load(allocator, path);
    defer allocator.free(third);
    try std.testing.expect((try get(third, "a")) == null);
    try std.testing.expectError(error.InvalidKey, save(path, third, "bad key", ""));
}
