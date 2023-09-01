#ifndef __HEADER_UNIQUE_MACRO
#define __HEADER_UNIQUE_MACRO

#include <iostream>

namespace snn::tmp {
    struct Name {
        std::string name;
        Name() = delete;
        Name(std::string&& name)
            : name(std::move(name)) {}
        Name(std::string const& name)
            : name{ name } {}
        Name(const Name& name)
            : name{ name.name } {}
        Name(Name&& name)
            : name{ std::move(name.name) } {}
    };

    struct Email {
        std::string email;
        Email() = delete;
        Email(std::string&& email)
            : email(std::move(email)) {}
        Email(std::string const& email)
            : email{ email } {}
        Email(const Email& email)
            : email{ email.email } {}
        Email(Email&& email)
            : email{ std::move(email.email) } {}
    };

    struct Person : public Name, public Email {
        unsigned age;
        Person() = delete;
        Person(std::string const& name, std::string const& email, unsigned age)
            : Name{ name }, Email{ email }, age{ age } {}
        Person(std::string&& name, std::string&& email, unsigned age)
            : Name{ std::move(name) },
            Email{ std::move(email) }, age{ age } {}
        Person(const Person& person)
            : Name{ person.name }, Email{ person.email }, age{ person.age } {}
        Person(Person&& person)
            : Name{ std::move(person.name) }, Email{ std::move(person.email) }, age{ person.age } {}
    };

    std::ostream& operator<<(std::ostream& out, Name const& n) {
        out << "Name('" << n.name << "')";
        return out;
    }

    std::ostream& operator<<(std::ostream& out, Email const& e) {
        out << "Email('" << e.email << "')";
        return out;
    }

    std::ostream& operator<<(std::ostream& out, Person const& p) {
        out << "Person('" << p.name << "', '" << p.email << "', " << p.age << ")";
        return out;
    }
}

#endif //__HEADER_UNIQUE_MACRO