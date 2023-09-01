#ifndef __SNN_CONTEXT_MANAGER_HPP__
#define __SNN_CONTEXT_MANAGER_HPP__

#include <string>

namespace snn::ctx
{
    template <typename Type>
    concept context_like = requires(Type t) { t.context_enter(); t.context_exit(); };

    template <context_like Type>
    struct context
    {
        context() = delete;
        context(context const &) = delete;
        context(context &&) = delete;
        void operator=(context const &) = delete;
        void operator=(context &&) = delete;
        context(Type &context)
            : _object{std::addressof(context)}
        {
            this->enter();
        }
        context(Type &&context)
            : _object{std::addressof(context)}
        {
            this->enter();
        }
        ~context() { this->exit(); }
        void enter()
        {
            if (this->entered)
                return;
            this->entered = true;
            this->exited = false;
            this->_object->context_enter();
        }
        void exit()
        {
            if (this->exited)
                return;
            this->exited = true;
            this->entered = false;
            this->_object->context_exit();
        }
        Type &object() { return *this->_object; }
        operator Type &() { return this->object(); }

    private:
        Type *_object;
        bool entered{false}, exited{false};
    };
}

#endif //__SNN_CONTEXT_MANAGER_HPP__