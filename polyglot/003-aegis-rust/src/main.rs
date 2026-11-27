use std::{path::Path, process::ExitCode, time::{SystemTime, UNIX_EPOCH}};

fn main() -> ExitCode {
    let args: Vec<_> = std::env::args_os().skip(1).collect();
    match args.as_slice() {
        [mode, path] if mode == "hash" => match aegis::fingerprint(Path::new(path)) {
            Ok(digest) => { println!("{digest}"); return ExitCode::SUCCESS; }
            Err(error) => eprintln!("{error}"),
        },
        [mode, path, expected] if mode == "check" => {
            let result = aegis::verify(Path::new(path), &expected.to_string_lossy());
            let seconds = SystemTime::now().duration_since(UNIX_EPOCH).unwrap_or_default().as_secs();
            let status = match &result { Ok(true) => "ok", Ok(false) => "changed", Err(_) => "error" };
            println!("time={seconds} path={path:?} status={status}");
            return match result {
                Ok(true) => ExitCode::SUCCESS,
                Ok(false) => ExitCode::from(1),
                Err(error) => { eprintln!("{error}"); ExitCode::from(2) }
            };
        }
        _ => eprintln!("usage: aegis hash FILE | aegis check FILE SHA256"),
    }
    ExitCode::from(2)
}
