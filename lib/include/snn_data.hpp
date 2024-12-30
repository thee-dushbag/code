#ifndef __SNN_DATA_HPP_
#define __SNN_DATA_HPP_

#ifdef LOG_SNN_DATA
# define __DATA_LOG(val) std::cout << "[Calling]: " << #val << '\n';
#include <iostream>
#else
# define __DATA_LOG(val)
#include <ostream>
#endif


namespace snn::utils {
    template<typename Type>
    struct data {
        ~data() { __DATA_LOG(Destructor) }
        data() : __data{} { __DATA_LOG(Default Constructor) }
        data(Type const& __d) : __data{ __d } { __DATA_LOG(Copy Value Constructor) }
        data(Type&& __d) : __data{ std::move(__d) } { __DATA_LOG(Move Value Constructor) }
        data(data const& __d) : __data{ __d.__data } { __DATA_LOG(Copy Constructor) }
        data(data&& __d) : __data{ std::move(__d.__data) } { __DATA_LOG(Move Constructor)  __d.__data = Type{}; }
        void operator=(data const& __d) { __DATA_LOG(Copy Assignment Operator)  this->__data = __d.__data; }
        void operator=(data&& __d) { __DATA_LOG(Move Assignment Operator)  this->__data = std::move(__d.__data); }
        void operator=(Type&& __d) { __DATA_LOG(Move Value Assignment Operator)  this->__data = std::move(__d); }
        void operator=(Type const& __d) { __DATA_LOG(Copy Value Assignment Operator)  this->__data = __d; }
        operator Type& () { __DATA_LOG(Type Cast Operator)  return this->__data; }
        bool operator<(Type const& __d) const noexcept { __DATA_LOG(Less than Operator) return this->__data < __d; }
        bool operator>(Type const& __d) const noexcept { __DATA_LOG(Greater than Operator) return this->__data > __d; }
        bool operator<=(Type const& __d) const noexcept { __DATA_LOG(Less than or Equalto Operator) return this->__data <= __d; }
        bool operator>=(Type const& __d) const noexcept { __DATA_LOG(Greater than or Equalto Operator) return this->__data >= __d; }
        bool operator==(Type const& __d) const noexcept { __DATA_LOG(Equalto Operator) return this->__data == __d; }
        bool operator!=(Type const& __d) const noexcept { __DATA_LOG(Not Equalto Operator) return this->__data != __d; }
        bool operator<(data const& __d) const noexcept { __DATA_LOG(Less than Operator) return this->__data < __d.__data; }
        bool operator>(data const& __d) const noexcept { __DATA_LOG(Greater than Operator) return this->__data > __d.__data; }
        bool operator<=(data const& __d) const noexcept { __DATA_LOG(Less than or Equalto Operator) return this->__data <= __d.__data; }
        bool operator>=(data const& __d) const noexcept { __DATA_LOG(Greater than or Equalto Operator) return this->__data >= __d.__data; }
        bool operator==(data const& __d) const noexcept { __DATA_LOG(Equalto Operator) return this->__data == __d.__data; }
        bool operator!=(data const& __d) const noexcept { __DATA_LOG(Not Equalto Operator) return this->__data != __d.__data; }
        data operator+(Type const& __d) const noexcept { __DATA_LOG(Plus Operator) return { this->__data + __d }; }
        data operator-(Type const& __d) const noexcept { __DATA_LOG(Subtract Operator) return { this->__data - __d }; }
        data operator/(Type const& __d) const noexcept { __DATA_LOG(Divide Operator) return { this->__data / __d }; }
        data operator*(Type const& __d) const noexcept { __DATA_LOG(Multiply Operator) return { this->__data * __d }; }
        data operator+(data const& __d) const noexcept { __DATA_LOG(Plus Operator) return { this->__data + __d.__data }; }
        data operator-(data const& __d) const noexcept { __DATA_LOG(Subtract Operator) return { this->__data - __d.__data }; }
        data operator/(data const& __d) const noexcept { __DATA_LOG(Divide Operator) return { this->__data / __d.__data }; }
        data operator*(data const& __d) const noexcept { __DATA_LOG(Multiply Operator) return { this->__data * __d.__data }; }
        void operator+=(Type const& __d) noexcept { __DATA_LOG(Plus Equal Operator) this->__data += __d; }
        void operator-=(Type const& __d) noexcept { __DATA_LOG(Subtract Equal Operator) this->__data -= __d; }
        void operator/=(Type const& __d) noexcept { __DATA_LOG(Divide Equal Operator) this->__data /= __d; }
        void operator*=(Type const& __d) noexcept { __DATA_LOG(Multiply Equal Operator) this->__data *= __d; }
        void operator+=(data const& __d) noexcept { __DATA_LOG(Plus Equal Operator) this->__data += __d.__data; }
        void operator-=(data const& __d) noexcept { __DATA_LOG(Subtract Equal Operator) this->__data -= __d.__data; }
        void operator/=(data const& __d) noexcept { __DATA_LOG(Divide Equal Operator) this->__data /= __d.__data; }
        void operator*=(data const& __d) noexcept { __DATA_LOG(Multiply Equal Operator) this->__data *= __d.__data; }
        friend std::ostream& operator<<(std::ostream& out, data const& __d) {
            out << "<data('" << __d.__data << "')>";
            return out;
        }

    private:
        Type __data;
    };
}

#endif //__SNN_DATA_HPP_
