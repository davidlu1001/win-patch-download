# Windows OS Patch Download

This script allows you to search and download Windows OS patch files from the Microsoft Update Catalog. You can specify the search keyword, month, and download path to customize the patch retrieval process.

## Prerequisites

- Python 3.x
- `pip` package manager

## Installation

1. Clone or download the repository.
2. Navigate to the project directory.
3. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script using the following command:

```
python win-patch-download.py [options]
```

### Options

- `-search`: Specify the search keyword. (Default: "Cumulative Update for Windows Server 2016 for x64-based Systems")
- `-month`: Specify the month in the format YYYY-MM. (Default: Current month)
- `-downloadpath`: Specify the download path for saving the patch files. (Default: "c:\cdrive")
- `-headless`: Run the script in headless mode. (Default: True)

### Examples

1. Run the script with default settings:

   ```
   python win-patch-download.py
   ```

2. Specify a specific month:

   ```
   python win-patch-download.py -month '2023-06'
   ```

3. Disable headless mode:

   ```
   python win-patch-download.py -month '2023-06' -headless False
   ```

4. Specify custom search keyword and download path:

   ```
   python win-patch-download.py -search 'Cumulative Update for Windows Server 2016 for x64-based Systems' -month '2023-06' -downloadpath 'C:\cdrive'
   ```

## Docker Support

The project includes Docker support, allowing you to run the script in a containerized environment. Follow the steps below to build and run the Docker container:

1. Build the Docker image:

   ```
   docker build -t win-patch-download .
   ```

2. Run the Docker container:

   ```
   # docker-compose
   docker-compose run win-patch-download -search 'Dynamic Update for Windows 11 for x64-based Systems' -month '2023-03' -downloadpath '/app/data'

   # docker
   docker run -v ./data:/app/data win-patch-download -search 'Dynamic Update for Windows 11 for x64-based Systems' -month '2023-06' -downloadpath "/app/data"
   ```

   This command will mount the local `./data` directory to the container's `/app/data` directory and pass the required arguments to the script.

## License

This project is licensed under the [MIT License](LICENSE).