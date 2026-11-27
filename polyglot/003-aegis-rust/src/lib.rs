use std::fs::{self, File};
use std::io::{self, BufReader};
use std::path::Path;
use std::process::{Command, Stdio};

pub fn fingerprint(path: &Path) -> io::Result<String> {
    if !fs::symlink_metadata(path)?.is_file() {
        return Err(io::Error::new(io::ErrorKind::InvalidInput, "expected regular file"));
    }
    let file = File::open(path)?;
    if !file.metadata()?.is_file() {
        return Err(io::Error::new(io::ErrorKind::InvalidInput, "expected regular file"));
    }
    let mut child = Command::new("sha256sum")
        .stdin(Stdio::piped()).stdout(Stdio::piped()).spawn()?;
    let copy_result = io::copy(&mut BufReader::new(file), &mut child.stdin.take().unwrap());
    let result = child.wait_with_output()?;
    copy_result?;
    if !result.status.success() {
        return Err(io::Error::other("sha256sum failed"));
    }
    let output = String::from_utf8(result.stdout).map_err(io::Error::other)?;
    let digest = output.split_whitespace().next().unwrap_or_default();
    validate_digest(digest)?;
    Ok(digest.to_owned())
}

fn validate_digest(digest: &str) -> io::Result<()> {
    if digest.len() != 64 || !digest.bytes().all(|b| b.is_ascii_hexdigit()) {
        return Err(io::Error::new(io::ErrorKind::InvalidInput, "invalid SHA-256"));
    }
    Ok(())
}

pub fn verify(path: &Path, expected: &str) -> io::Result<bool> {
    validate_digest(expected)?;
    Ok(fingerprint(path)?.eq_ignore_ascii_case(expected))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn detects_changes() {
        let dir = std::env::temp_dir().join(format!("aegis-test-{}", std::process::id()));
        fs::create_dir(&dir).unwrap();
        let path = dir.join("sample");
        fs::write(&path, b"abc").unwrap();
        let digest = fingerprint(&path).unwrap();
        assert_eq!(digest, "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
        fs::write(&path, b"changed").unwrap();
        assert!(!verify(&path, &digest).unwrap());
        assert!(verify(&path, "bad").is_err());
        assert!(fingerprint(&dir).is_err());
        fs::remove_dir_all(dir).unwrap();
    }
}
