from analyzer.models import AccountObservation
from analyzer.scoring import calculate_score


def get_username() -> str:
    while True:
        username = input("Username: @").strip().lstrip("@")

        if username:
            return username

        print("Username cannot be empty. Try again.")


def get_float(
    prompt: str,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    while True:
        raw_value = input(prompt).strip()

        try:
            value = float(raw_value)
        except ValueError:
            print("Enter only a number, such as 18 or 0.71.")
            continue

        if minimum is not None and value < minimum:
            print(f"Enter a number greater than or equal to {minimum}.")
            continue

        if maximum is not None and value > maximum:
            print(f"Enter a number less than or equal to {maximum}.")
            continue

        return value


def get_integer(prompt: str, minimum: int = 0) -> int:
    while True:
        raw_value = input(prompt).strip()

        try:
            value = int(raw_value)
        except ValueError:
            print("Enter only a whole number, such as 2 or 10.")
            continue

        if value < minimum:
            print(f"Enter a whole number greater than or equal to {minimum}.")
            continue

        return value


def analyze_account() -> None:
    print("\n" + "=" * 44)
    print("Threads Agent Observatory")
    print("Version 0.0.2")
    print("=" * 44)

    username = get_username()

    posts_per_day = get_float(
        "Average posts per day: ",
        minimum=0,
    )

    repeated_phrases = get_integer(
        "Repeated phrases observed: ",
        minimum=0,
    )

    similarity_score = get_float(
        "Language similarity score (0.0 to 1.0): ",
        minimum=0.0,
        maximum=1.0,
    )

    account = AccountObservation(
        username=username,
        posts_per_day=posts_per_day,
        repeated_phrases=repeated_phrases,
        similarity_score=similarity_score,
    )

    score = calculate_score(account)

    print("\n" + "=" * 44)
    print("Research Report")
    print("=" * 44)
    print(f"Username: @{account.username}")
    print(f"Posts per day: {account.posts_per_day}")
    print(f"Repeated phrases: {account.repeated_phrases}")
    print(f"Language similarity: {account.similarity_score}")
    print(f"Observable Pattern Score: {score}/100")
    print("=" * 44)
    print("This score does not prove whether an account is automated.")


def main() -> None:
    while True:
        analyze_account()

        again = input("\nAnalyze another account? (y/n): ").strip().lower()

        if again not in {"y", "yes"}:
            print("\nSession ended.\n")
            break


if __name__ == "__main__":
    main()
