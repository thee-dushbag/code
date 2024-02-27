#ifndef _HI_HPP
#define _HI_HPP

// Wrap everything into a nice namespace for global cleanliness
namespace hi {
  extern "C" {
#define this _this // Deal with the invalid use of this in hi.h
#define class _class // Deal with the invalid use of class in hi.h
# include "hi.h" // The code with the identifiers this and class as variables
#undef this // Prevent from further substitutions of this to _this
#undef class // Prevent from further substitutions of class to _class
  }
}

#endif //_HI_HPP
