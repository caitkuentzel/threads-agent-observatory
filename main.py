from analyzer.models import AccountObservation
from analyzer.scoring import calculate_score
from analyzer.storage import save_observation


def get_username() -> str:
    while True:
        username = input("Username: @").strip().lstrip("@")
        if username:
            return username
        print("Username cannot be empty.")


def get_float(prompt: str, minimum=None, maximum=None):
    while True:
        try:
            value = float(input(prompt))

            if minimum is not None and value < minimum:
                print(f"Enter a value greater than or equal to {minimum}.")
                continue

            if maximum is not None and value > maximum:
                print(f"Enter a value less than or equal to {maximum}.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")


def get_integer(prompt: str):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")


def analyze_account():

    print("\n" + "=" * 44)
    print("Threads Agent Observatory")
    print("Version 0.0.3")
    print("=" * 44)

    username = get_username()

    posts_per_day = get_float(
        "Average posts per day: ",
        minimum=0,
    )

    repeated_phrases = get_integer(
        "Repeated phrases observed: "
    )

    similarity_score = get_float(
        "Language similarity score (0.0 - 1.0): ",
        minimum=0,
        maximum=1,
    )

    account = AccountObservation(
        username=username,
        posts_per_day=posts_per_day,
        repeated_phrases=repeated_phrases,
        similarity_score=similarity_score,
    )

    score = calculate_score(account)

    data_file = save_observation(account, score)

    print("\n" + "=" * 44)
    print("Research Report")
    print("=" * 44)
    print(f"Username: @{account.username}")
    print(f"Posts per day: {account.posts_per_day}")
    print(f"Repeated phrases: {account.repeated_phrases}")
    print(f"Similarity: {account.similarity_score}")
    print(f"Observable Pattern Score: {score}/100")
    print("=" * 44)
    print(f"Saved to: {data_file}")
    print("Observation recorded successfully.")


def main():

    while True:

        analyze_account()

        again = input("\nAnalyze another account? (y/n): ").lower()

        if again != "y":
            print("\nGoodbye!\n")
            break


if __name__ == "__main__":
    main()
