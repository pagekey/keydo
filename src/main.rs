use std::io;
use std::process;
use std::env;

#[test]
fn test_something() {
    println!("testing");
    assert!(3==3);
}

fn main() {
    let mut argv = env::args();
    while let Some(arg) = argv.next() {
        println!("hey arg {}",arg);
    }
    let mut stout = io::stdout;
    stdout.flush().expect("Failed to flush stdout");
    loop {
        let mut buffer = [0u8; 1024];
        match process::command(&["read"]).stdout(std::io::stderr())
            .stdout(process::stdin())
            .stderr(process::stdout())
            .output()
            .expect("Failed to read stdin") {
                Ok((stderr, stdout, _)) => println!("{:?}", stderr),
                Err(err) => println!("Error: {:?}: {:?}", err, buffer),
            }
    }
}
