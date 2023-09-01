#ifndef __TMP_INHERITANCE_SNN_HPP_
#define __TMP_INHERITANCE_SNN_HPP_

#include <iostream>

namespace snn::inhe_tmps {
    struct Callable {
        virtual void call() = 0;
    };

    struct ChildOne: Callable {
        void whoOne() {
            std::cout << "Hello There: This is whoOne()\n";
        }
        void call() {
            whoOne();
        }
    };

    struct ChildThree: Callable {
        void whoThree() {
            std::cout << "Hello There: This is whoThree()\n";
        }
        void call() {
            whoThree();
        }
    };

    struct ChildTwo: Callable {
        void whoTwo() {
            std::cout << "Hello There: This is whoTwo()\n";
        }
        void call() {
            whoTwo();
        }
    };

    template<typename T>
    struct Data: Callable {
        T data;
        Data(T const &data): data{data} {}
        void showData() {
            std::cout << "I have: data='" << this->data << "'\n";
        }
        void call() {
            showData();
        }
    };
}

#endif //__TMP_INHERITANCE_SNN_HPP_