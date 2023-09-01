#ifndef __SNN_LINE_PROCESSOR_
#define __SNN_LINE_PROCESSOR_

#include <queue>
#include <iostream>
#include <future>
#include <unordered_map>
#include <functional>
#include <snn_bqueue.hpp>
#include <variant>

namespace snn {
    template<typename K, typename V>
    using _map_type = std::unordered_map<K, V>;


    template<typename T>
    struct Line {
        typedef T value_type;
        constexpr Line() : value{} {}
        constexpr Line(T const& value)
            : value{ value } {}
        constexpr Line(T&& value)
            : value{ std::move(value) } {}
        void set_value(value_type&& v)
        { value = std::move(v); }
        void set_value(value_type const &v)
        { value = v; }
        void set_value(Line&& v)
        { value = std::move(v.value); }
        void set_value(Line const &v)
        { value = v.value; }
        value_type const& get_value() const
        { return value; }

    private:
        value_type value;
    };

    template<typename T>
    std::ostream& operator<<(std::ostream& out, Line<T> const& l)
    {
        out << "Line('" << l.get_value() << "')"; return out;
    }

    template<typename K, typename V>
    struct SpecialLine {
        typedef K key_type;
        typedef V value_type;
        SpecialLine() = delete;
        constexpr SpecialLine(K const& k, V const& v)
            : key{ k }, value{ v } {}
        constexpr SpecialLine(K&& k, V&& v)
            : key{ std::move(k) }, value{ std::move(v) } {}
        void set_value(V const& v) { value = v; }
        void set_value(V&& v) { value = std::move(v); }
        value_type const& get_value() const
        {
            return value;
        }
        key_type const& get_key() const
        {
            return key;
        }
        std::pair<key_type, value_type> get() const
        {
            return { key, value };
        }
    private:
        key_type key;
        value_type value;
    };

    template<typename K, typename V>
    std::ostream& operator<<(std::ostream& out, SpecialLine<K, V> const& l)
    {
        out << "SpecialLine('" << l.get_key() << "', '" << l.get_value() << "')"; return out;
    }

    template<typename K, typename V>
    using _sline_callable = typename std::function<void(SpecialLine<K, V>)>;

    template<typename L, typename K, typename V = L>
    struct Processor {
        typedef L line_type;
        typedef K key_type;
        typedef V value_type;
        typedef _map_type<key_type, _sline_callable<key_type, value_type>> map_type;
        map_type special_map;
        void add_special(key_type const& key, _sline_callable<key_type, value_type> const& callback)
        {
            special_map[key] = callback;
        }
        void operator()(Line<line_type> const& line)
        {
            on_line(line);
        }
        void operator()(SpecialLine<key_type, value_type> const& sline)
        {
            if (special_map.contains(sline.get_key())) special_map.at(sline.get_key())(sline);
        }
        virtual void on_line(Line<line_type> const& line)
        { std::cout << "Processing: " << line << '\n'; }
    };

    template <typename ProcessorType, typename L, typename K, typename V>
    concept ProcessEntity = requires (ProcessorType pro)
    { { pro(std::declval<Line<L>>()) } -> std::same_as<void>;
    { pro(std::declval<SpecialLine<K, V>>()) } -> std::same_as<void>;  };

    template<typename LineType, typename KeyType, typename _Processor = Processor<LineType, KeyType, LineType>, typename ValueType = LineType>
    requires ProcessEntity<_Processor, LineType, KeyType, ValueType>
    struct Belt {
        typedef std::variant<Line<LineType>, SpecialLine<KeyType, ValueType>> belt_item_type;
        enum class _state : uint { alive, dead };

        void start() { this->_start(); }
        void stop() { this->_stop(); }
        bool running() const { return this->_belt_state == _state::alive; }
        Belt() : _processor{}, _cache{}, _belt{}, _belt_state{ _state::dead } {}
        Belt(_Processor const &p): _processor{p}, _cache{}, _belt{}, _belt_state{ _state::dead } {}
        Belt(_Processor &&p): _processor{std::move(p)}, _cache{}, _belt{}, _belt_state{ _state::dead } {}
        void send(belt_item_type const &item) { this->_send(item); }
        void send_line(Line<LineType> const &line)
        { this->_send(line); }
        void send_sline(SpecialLine<KeyType, ValueType> const &sline)
        { this->_send(sline);}
        void add_special(KeyType const &key, _sline_callable<KeyType, ValueType> const &callback)
        { this->_processor.add_special(callback); }
        virtual ~Belt() { this->wait(); this->stop(); }
        void wait() const { while(this->running() and not this->_belt.empty()) {} }

    private:
        _Processor _processor;
        std::queue<belt_item_type> _cache;
        bqueue<belt_item_type> _belt;
        std::thread _runner;
        _state _belt_state;

        void _run() {
            std::future<belt_item_type> item;
            try {
                while (this->running()) {
                    item = this->_belt.pop();
                    std::visit(this->_processor, item.get());
                }
            } catch (closing_bqueue const& error) {
                if (item.valid()) this->_cache.push(item.get());
            }
        }
        void _start() {
            if (this->running()) return;
            this->_belt_state = _state::alive;
            this->_belt = bqueue(std::move(this->_cache));
            this->_runner = std::thread([&] { this->_run(); });
        }
        void _send(belt_item_type const &item) {
            if (this->running())
                this->_belt.push(item);
            else this->_cache.push(item);
        }
        void _stop() {
            if (not this->running()) return;
            this->_belt_state = _state::dead;
            this->_cache = this->_belt.close();
            this->_runner.join();
        }
    };
}

#endif //__SNN_LINE_PROCESSOR_