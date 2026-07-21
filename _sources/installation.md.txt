# Installation

## Prerequisites

- Python 3.13 or higher
- MySQL client libraries
- MySQL database with the `g4public` schema

## Installing my-g4public-orm

You can install `my-g4public-orm` using pip:

```bash
pip install my-g4public-orm
```

Or if you're using uv:

```bash
uv pip install my-g4public-orm
```

## Installing MySQL Client Libraries

The ORM uses `mysqlclient` as the database driver, which requires MySQL client libraries to be installed on your system.

### macOS

Using Homebrew:

```bash
brew install mysql-client
export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"
pip install mysqlclient
```

### Ubuntu/Debian

```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
pip install mysqlclient
```

### CentOS/RHEL

```bash
sudo yum install mysql-devel python3-devel gcc
pip install mysqlclient
```

## Configuration

The ORM uses environment variables for database configuration. Create a `.env` file in your project root:

```bash
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=g4public
DB_CHARSET=utf8mb4
```

See `.env.example` for all available configuration options.