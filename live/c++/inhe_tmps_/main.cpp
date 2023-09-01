#include "base.hpp"
#include <iostream>
#include <vector>

using namespace snn::inhe_tmps;

auto main(int argc, char **argv) -> int {
    ChildOne one;
    ChildTwo two;
    ChildThree three;
    std::vector<Callable *> calls{&one, &two, &three};
    for (auto const &call: calls)
        call->call();
    Data<std::string> ds{"Simon Nganga"};
    Data<int> di{5052};
    Data<float> df{45.6f};
    std::vector<Callable *> datas{&ds, &di, &df};
    for (auto const &data: datas)
        data->call();
}