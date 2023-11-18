fn main() {
    println!("Rust: Hello World");
    let end = 10_000_000;
    for i in 0..end {
        print!("\rRust: Line {}", i);
    }
    println!("\rRust: Done.... {}", end);
}