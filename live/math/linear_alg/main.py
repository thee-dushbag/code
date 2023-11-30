from vectors import Vector, dot_product_algebraic, vector_angle


def main():
    v = Vector([1, 2, 3])
    print(f"{v}.magnitude = {v.magnitude}")
    u = Vector([4, 5, 6])
    print(f"dot({v}, {u}) = {dot_product_algebraic(v, u)}")
    print(f"dot({u}, {v}) = {dot_product_algebraic(u, v)}")
    print(f'angle({v}, {u}) = {vector_angle(v, u)}')


if __name__ == "__main__":
    main()
