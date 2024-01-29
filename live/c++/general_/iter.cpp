#include <iostream>
#include <type_traits>
#include <concepts>

namespace snn {
  struct rstate {
    enum class limit : bool { lower, upper };
    rstate() = delete;
    rstate(int stop, limit lim)
      : current{ stop }, step{ bool(lim) } { }
    rstate(int start, int step)
      : current{ start }, step{ step } { }
    int operator*() const { return current; }
    bool operator==(rstate const &stop) const {
      return stop.step ?
        current >= stop.current :
        current <= stop.current;
    }
    rstate &operator++() {
      current += step;
      return *this;
    }
  private:
    int current, step;
  };

  struct range {
    range() = delete;
    range(int stop)
      : start{ 0 }, stop{ stop }, step{ 1 } { }
    range(int start, int stop)
      : start{ start }, stop{ stop }, step{ 1 } { }
    range(int start, int stop, int step)
      : start{ step < 0 ? stop : start },
      stop{ step > 0 ? stop : start },
      step{ step < 0 ? -step : step } { }
    range(range const &rg)
      : start{ rg.start }, stop{ rg.stop }, step{ rg.step } { }
    rstate rend() const { return { start - step, bound::lower }; }
    rstate rbegin() const { return { stop - step, -step }; }
    rstate end() const { return { stop, bound::upper }; }
    rstate begin() const { return { start, step }; }
  private:
    using bound = rstate::limit;
    int start, stop, step;
  };

  template<typename Iterator>
  struct reverse {
    reverse() = delete;
    reverse(Iterator iter) : iter{ iter } { }
    decltype(auto) begin() const { return iter.rbegin(); }
    decltype(auto) end() const { return iter.rend(); }
    decltype(auto) rbegin() const { return iter.begin(); }
    decltype(auto) rend() const { return iter.end(); }
    operator Iterator() const { return iter; }
  private:
    Iterator iter;
  };
}

auto main(int argc, char **argv) -> int {
  snn::range one2ten{ 1, 11 };
  std::cout << "FORWARD" << '\n';
  for (int i : one2ten)
    std::cout << i << " * " << i << " = " << i * i << '\n';
  std::cout << "BACKWARD" << '\n';
  for (int r : snn::reverse{ one2ten })
    std::cout << r << " ^ 2 = " << r * r << '\n';
}
