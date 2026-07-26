from analyzer.models import AccountObservation
from analyzer.reader import (
    export_text_report,
    print_observations,
    print_search_results,
    print_summary,
)
from analyzer.scoring import calculate_score
from analyzer.storage import save_observation

VERSION = "0.1.0"


def get_username(prompt: str = "Username: @") -> str:
    while True:
        username = input(prompt).strip().lstrip("@")
        if username:
            return username
        print("Username cannot be empty.")


def get_float(
    prompt: str,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if minimum is not None and value < minimum:
            print(f"Enter a value greater than or equal to {minimum}.")
            continue

        if maximum is not None and value > maximum:
            print(f"Enter a value less than or equal to {maximum}.")
            continue

        return value


def get_integer(prompt: str, minimum: int | None = None) -> int:
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue

        if minimum is not None and value < minimum:
            print(f"Enter a value greater than or equal to {minimum}.")
            continue

        return value


def analyze_account() -> None:
    print("\n" + "=" * 44)
    print("New Account Observation")
    print("=" * 44)

    account = AccountObservation(
        username=get_username(),
        posts_per_day=get_float("Average posts per day: ", minimum=0),
        repeated_phrases=get_integer(
            "Repeated phrases observed: ", minimum=0
        ),
        similarity_score=get_float(
            "Language similarity score (0.0 - 1.0): ",
            minimum=0,
            maximum=1,
        ),
    )

    score = calculate_score(account)
    data_file = save_observation(account, score)

    print("\n" + "=" * 44)
    print("Research Report")
    print("=" * 44)
    print(f"Username: @{account.username}")
    print(f"Posts per day: {account.posts_per_day}")
    print(f"Repeated phrases: {account.repeated_phrases}")
    print(f"Similarity: {account.similarity_score:.2f}")
    print(f"Observable Pattern Score: {score:.2f}/100")
    print("=" * 44)
    print("This score describes observable patterns; it does not prove automation.")
    print(f"Saved to: {data_file.relative_to(data_file.parent.parent)}")


def print_menu() -> None:
    print("\n" + "=" * 50)
    print(f"Threads Agent Observatory — Version {VERSION}")
    print("=" * 50)
    print("1. Analyze a new account")
    print("2. View all saved observations")
    print("3. Search account history")
    print("4. View research summary")
    print("5. Export text report")
    print("6. Exit")
    print("=" * 50)


def main() -> None:
    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            analyze_account()
        elif choice == "2":
            print_observations()
        elif choice == "3":
            username = get_username("Search username: @")
            print_search_results(username)
        elif choice == "4":
            print_summary()
        elif choice == "5":
            report_file = export_text_report()
            if report_file is None:
                print("\nNo saved observations are available to export.")
            else:
                print(
                    "\nReport exported to: "
                    f"{report_file.relative_to(report_file.parent.parent)}"
                )
        elif choice == "6":
            print("\nGoodbye!\n")
            break
        else:
            print("\nPlease choose a number from 1 through 6.")


if __name__ == "__main__":
    main()

