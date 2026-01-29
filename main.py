import os
import build_database


def main():
    # Downloads milex data, build database
    build_database.main()

    # Generate analysis figures
    print("Generating figures...")

    # Compile report
    print("Compiling report...")
    filename = '"Arms In and Out of Australia.pdf"'
    os.system(f"typst compile report.typ {filename}")

    print("Done.")


if __name__ == "__main__":
    main()
