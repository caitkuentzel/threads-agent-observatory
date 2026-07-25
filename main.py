from analyzer.models import AccountObservation
from analyzer.scoring import calculate_score


def main():

    account = AccountObservation(
        username="example_account",
        posts_per_day=14,
        repeated_phrases=3,
        similarity_score=0.82
    )

    score = calculate_score(account)

    print("=" * 40)
    print("Threads Agent Observatory")
    print("=" * 40)
    print(f"Username: @{account.username}")
    print(f"Observable Pattern Score: {score}/100")
    print("=" * 40)


if __name__ == "__main__":
    main()
