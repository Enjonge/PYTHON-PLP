
def calculate_discount(price, discount_percent):

    if discount_percent >= 20:
        return price * (1 - discount_percent / 100)
    else:
        return price


def main():
    try:
        # Get user input
        price = float(input("Enter the original price: Ksh "))
        discount_percent = float(input("Enter the discount percentage (0-100): "))

        # Validate input
        if price < 0:
            print("Price cannot be negative.")
            return
        if discount_percent < 0 or discount_percent > 100:
            print("Discount percentage must be between 0 and 100.")
            return

        # Calculate final price
        final_price = calculate_discount(price, discount_percent)

        # Display result
        if discount_percent >= 20:
            print(f"\nOriginal price: Ksh{price:.2f} ")
            print(f"Discount applied: {discount_percent}%")
            print(f"Final price after discount: Ksh{final_price:.2f} ")
        else:
            print(f"\nNo discount applied (needs 20% or higher). Price remains: Ksh{price:.2f} ")

    except ValueError:
        print("Invalid input. Please enter numeric values.")


if __name__ == "__main__":
    main()