import uvicorn
import controller


def main():
    uvicorn.run("controller:app", host="0.0.0.0", port=9000, reload=True)


if __name__ == "__main__":
    main()
