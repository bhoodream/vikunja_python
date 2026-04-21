# Vikunja Python CLI

A simple and elegant command-line interface for viewing tasks from your [Vikunja](https://vikunja.io/) instance.

## Features

- 🚀 **Fast Task Viewing**: Quickly see your tasks grouped by project.
- 🎯 **Flexible Selection**: Choose a specific project via CLI arguments, environment variables, or interactive menu.
- 📅 **Smart Formatting**: Overdue tasks are highlighted in red, and dates are formatted for readability.
- 🎨 **Beautiful UI**: Powered by `rich` for a clean, colorful terminal experience.

## Installation

1. **Clone the repository**:
  ```bash
   git clone https://github.com/bhoodream/vikunja_python.git
   cd vikunja_python
  ```
2. **Set up a virtual environment**:
  ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
3. **Install dependencies**:
  ```bash
   pip install -r requirements.txt
  ```

## Configuration

The CLI can be configured using environment variables or a `.env` file.

1. Copy the example environment file:
  ```bash
   cp .env.example .env
  ```
2. Edit `.env` and provide your Vikunja URL and API Token:
  ```env
   VIKUNJA_URL=https://your-vikunja-instance.com
   VIKUNJA_TOKEN=your_api_token_here
  ```

## Usage

### Basic Usage

Run the script to see an interactive project selector:

```bash
python vikunja_cli.py
```

### Select a Specific Project

You can specify a project by its ID or Title:

```bash
python vikunja_cli.py --project "My Project"
# OR
python vikunja_cli.py --project 42
```

### Show All Projects

To see tasks from all projects at once:

```bash
python vikunja_cli.py --project all
```

### Environment Variables

You can also set the default project in your `.env` file:

```env
VIKUNJA_PROJECT=all
```

## Development

- **Language**: Python 3.8+
- **Key Libraries**: `click`, `requests`, `rich`, `questionary`, `python-dotenv`

## License

MIT