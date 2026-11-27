const std = @import("std");
const store = @import("store.zig");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const args = try std.process.argsAlloc(allocator);
    if (args.len < 4 or args.len > 5) return usage();
    const command = args[1];
    const path = args[2];
    const key = args[3];
    const data = try store.load(allocator, path);
    if (args.len == 4 and std.mem.eql(u8, command, "get")) {
        const value = (try store.get(data, key)) orelse return error.KeyNotFound;
        try std.io.getStdOut().writer().print("{s}\n", .{value});
    } else if (args.len == 5 and std.mem.eql(u8, command, "put")) {
        try store.save(path, data, key, args[4]);
    } else if (args.len == 4 and std.mem.eql(u8, command, "del")) {
        try store.save(path, data, key, null);
    } else return usage();
}

fn usage() error{InvalidArguments} {
    std.debug.print("usage: vulcan get|del FILE KEY | vulcan put FILE KEY VALUE\n", .{});
    return error.InvalidArguments;
}
