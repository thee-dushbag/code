#include <iostream>
#include "events.hpp"
#include <chrono>
#include <mutex>
std::mutex plock;
unsigned N = 5;

template <typename Type>
void print(Type obj)
{
    plock.lock();
    std::cout << "[thread: " << std::this_thread::get_id() << "] " << obj;
    plock.unlock();
}

struct say_hi : public snn::events::functor
{
    say_hi(std::string const &name) : name{name} {}
    void sayhi() { print("Hello " + this->name + ", how was your day?\n"); }
    void operator()() { this->sayhi(); }
    void set(std::string const &name) { this->name = name; }

private:
    std::string name;
};

struct add : public snn::events::functor
{
    add(long x, long y) : x{x}, y{y} {}
    void operator()()
    {
        std::this_thread::sleep_for(std::chrono::seconds(N));
        print(std::to_string(this->x) + " + " + std::to_string(this->y) + " = " + std::to_string(this->x + this->y) + "\n");
    }
    void set(long x, long y)
    {
        this->x = x;
        this->y = y;
    }

private:
    long x, y;
};

struct sub : public snn::events::functor
{
    sub(long x, long y) : x{x}, y{y} {}
    void operator()()
    {
        std::this_thread::sleep_for(std::chrono::seconds(N));
        print(std::to_string(this->x) + " - " + std::to_string(this->y) + " = " + std::to_string(this->x - this->y) + "\n");
    }
    void set(long x, long y)
    {
        this->x = x;
        this->y = y;
    }

private:
    long x, y;
};

struct mul : public snn::events::functor
{
    mul(long x, long y) : x{x}, y{y} {}
    void operator()()
    {
        std::this_thread::sleep_for(std::chrono::seconds(N));
        print(std::to_string(this->x) + " * " + std::to_string(this->y) + " = " + std::to_string(this->x * this->y) + "\n");
    }
    void set(long x, long y)
    {
        this->x = x;
        this->y = y;
    }

private:
    long x, y;
};

auto main(void) -> int
{
    snn::events::event event;
    say_hi p1{"Simon"};
    say_hi p2{"Nganga"};
    say_hi p3{"Njoroge"};
    say_hi p4{"Faith"};
    say_hi p5{"Njeri"};
    say_hi p6{"Wanjiru"};
    event.subscribe("sayhi", &p1);
    event.subscribe("sayhi", &p2);
    event.subscribe("sayhi", &p3);
    event.subscribe("sayhi", &p4);
    event.subscribe("sayhi", &p5);
    event.subscribe("sayhi", &p6);
    event.emit("sayhi");
    p1.set("Lydia");
    p2.set("Samuel");
    p3.set("Karanja");
    p4.set("Peter");
    p5.set("Mbiu");
    p6.set("Kimotho");
    event.emit("sayhi");
    add a{100, 50};
    mul m{12, 4};
    sub s{100, 15};
    event.subscribe("math-them", &a);
    event.subscribe("math-them", &s);
    event.subscribe("math-them", &m);
    event.emit("math-them");
    a.set(300, 400);
    s.set(90, 67);
    m.set(12, 13);
    event.emit("math-them");
}