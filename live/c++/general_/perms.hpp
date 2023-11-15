#ifndef __SNN_PERMISSIONS_TEST_HPP_
#define __SNN_PERMISSIONS_TEST_HPP_

#include <iostream>

namespace snn::perms {
  enum class Perm : u_short {
    NONE = 0L,
    READ = 1L << 0,
    WRITE = 1L << 1,
    EXECUTE = 1L << 2
  };

  std::ostream &operator<<(std::ostream &out, Perm const &p) {
    std::string opname = "Perm::";
    switch (p) {
      using enum Perm;
    case NONE:
      opname += "NONE";
      break;
    case READ:
      opname += "READ";
      break;
    case WRITE:
      opname += "WRITE";
      break;
    case EXECUTE:
      opname += "EXECUTE";
      break;
    default:
      opname = "Perm::<UNKNOWN>";
      break;
    }
    return out << '<' << opname << ' ' << u_short(p) << '>';
  }

  struct Permission {
    Permission() : perm{ u_short(Perm::NONE) } { }
    Permission(u_short p): perm { p } { }
    Permission(Perm const &val) : perm{ u_short(val) } { }
    Permission(Permission const &p) : perm{ p.perm } { }
    Permission(Permission &&p) : perm{ std::move(p.perm) } {
      p.perm = u_short(Perm::NONE);
    }
    bool operator==(Permission const &p) const {
      return p.perm == perm;
    }
    bool operator!=(Permission const &p) const {
      return p.perm != perm;
    }
    void operator=(Permission const &p) {
      perm = p.perm;
    }
    void operator=(Permission &&p) {
      perm = p.perm;
      p.perm = u_short(Perm::NONE);
    }
    bool operator==(Perm const &p) const {
      return has(p);
    }
    bool has(Perm const &p) const {
      return (perm & u_short(p)) == u_short(p);
    }
    Permission &give(Perm const &p) {
      perm |= u_short(p); return *this;
    }
    Permission &take(Perm const &p) {
      if (has(p)) perm ^= u_short(p);
      return *this;
    }
    bool only(Perm const &p) const {
      return perm == u_short(p);
    }
    bool has(u_short const &p) const {
      return (perm & p) == u_short(p);
    }
    Permission &give(u_short const &p) {
      perm |= p; return *this;
    }
    Permission &take(u_short const &p) {
      if (has(p)) perm ^= p;
      return *this;
    }
    Permission &toggle(u_short const &p) {
      perm ^= p; return *this;
    }
    Permission &toggle(Perm const &p) {
      perm ^= u_short(p); return *this;
    }
    bool only(u_short const &p) const {
      return perm == p;
    }
    operator bool() const {
      return not only(Perm::NONE);
    }
    u_short value() const { return perm; }
    operator u_short() const { return perm; }
  private:
    u_short perm;
  };

  std::ostream &operator<<(std::ostream &out, Permission const &p) {
    using enum Perm;
    out << "Permission(perm=" << p.value() << ", perms=[";
    if (p) {
      if (p.has(READ)) out << READ << ',';
      if (p.has(WRITE)) out << WRITE << ',';
      if (p.has(EXECUTE)) out << EXECUTE << ',';
    }
    else out << NONE;
    return out << "])";
  }
}

#endif //__SNN_PERMISSIONS_TEST_HPP_