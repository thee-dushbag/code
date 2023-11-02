#ifndef __HEADER_UNIQUE_MACRO
#define __HEADER_UNIQUE_MACRO

#include <concepts>
#include <type_traits>

namespace snn::functional {
    namespace __detail {
        class _IncompleteType;
        using _Sentinel = _IncompleteType;
    }
    using unknown_t = __detail::_IncompleteType;

    template<typename _Sign, typename _Class>
    requires std::is_member_function_pointer_v<_Sign _Class::*>
    class MemFunc {
        using function_sig = _Sign _Class::*;
        template<typename..._Args>
        using return_t = std::invoke_result_t<_Sign, _Args...>;
        function_sig member_function;

    public:
        MemFunc() = delete;

        MemFunc(_Sign _Class::* const &memfn)
        : member_function{memfn} {}

        MemFunc(_Sign _Class::* &&memfn)
        : member_function{std::move(memfn)} {}

        template<typename _Cls, typename..._Args>
        requires (std::same_as<return_t<_Args...>, void>)
        void operator()(_Cls &&instance, _Args &&...args)
        { (std::forward<_Cls>(instance).*this->member_function)
        (std::forward<_Args>(args) ...); }

        template<typename _Cls, typename..._Args>
        requires (not std::same_as<return_t<_Args...>, void>)
        return_t<_Args...> operator()(_Cls &&instance, _Args &&...args)
        { return (std::forward<_Cls>(instance).*this->member_function)
        (std::forward<_Args>(args) ...); }
    };

    template<typename _Sig, typename _Class, typename _Cls, typename... _Args>
    requires std::same_as<std::invoke_result_t<_Sig, _Args...>, void>
    void call_member(_Sig _Class::* &&memfn, _Cls &&instance, _Args &&...args)
    { (std::forward<_Class>(instance).*memfn)(std::forward<_Args>(args) ...); }

    template<typename _Sig, typename _Class, typename _Cls, typename ..._Args>
    requires (not std::same_as<std::invoke_result_t<_Sig, _Args...>, void>)
    decltype(auto) call_member(_Sig _Class::* &&memfn, _Cls &&instance, _Args &&...args)
    { return (std::forward<_Cls>(instance).*memfn)(std::forward<_Args>(args) ...); }

    template<typename _Sign, typename _Class>
    MemFunc<_Sign, _Class> mem_fn(_Sign _Class::* &&memfn)
    { return std::forward<_Sign _Class::*>(memfn); }
}

#endif //__HEADER_UNIQUE_MACRO