#include <iostream>

auto main(int argc, char **argv) -> int {
    std::cout << "C++: Hello World\n";
    int end = 10'000'000;
    for(int i = 0; i < end; i++)
        std::cout << "\rC++: Line " << i;
    std::cout << "\rC++: Done.... " << end << '\n';
}