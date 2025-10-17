# =============================================================================
# POST, INTERACTION & REEL SERVICE - DOCKER SCRIPTS
# =============================================================================
# Scripts để quản lý Docker containers

#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=============================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=============================================================================${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Docker and Docker Compose are available"
}

# Build and start all services
start_all() {
    print_header "Starting Post, Interaction & Reel Service"
    
    check_docker
    
    print_status "Building and starting all services..."
    docker-compose up -d --build
    
    print_status "Waiting for services to be ready..."
    sleep 10
    
    print_status "Services started successfully!"
    print_status "API: http://localhost:8000"
    print_status "API Docs: http://localhost:8000/docs"
    print_status "MinIO Console: http://localhost:9001"
}

# Stop all services
stop_all() {
    print_header "Stopping Post, Interaction & Reel Service"
    
    print_status "Stopping all services..."
    docker-compose down
    
    print_status "Services stopped successfully!"
}

# Restart all services
restart_all() {
    print_header "Restarting Post, Interaction & Reel Service"
    
    print_status "Restarting all services..."
    docker-compose restart
    
    print_status "Services restarted successfully!"
}

# Show logs
show_logs() {
    print_header "Showing Application Logs"
    
    docker-compose logs -f app
}

# Show status
show_status() {
    print_header "Service Status"
    
    docker-compose ps
}

# Run tests
run_tests() {
    print_header "Running Tests"
    
    print_status "Running tests in container..."
    docker-compose exec app pytest app/tests/ -v
    
    if [ $? -eq 0 ]; then
        print_status "All tests passed!"
    else
        print_error "Some tests failed!"
        exit 1
    fi
}

# Initialize database
init_db() {
    print_header "Initializing Database"
    
    print_status "Initializing database..."
    docker-compose exec app python app/db/init_db.py init
    
    print_status "Database initialized successfully!"
}

# Clean up
cleanup() {
    print_header "Cleaning Up"
    
    print_warning "This will remove all containers, volumes, and images. Are you sure? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Stopping and removing containers..."
        docker-compose down -v
        
        print_status "Removing images..."
        docker-compose down --rmi all
        
        print_status "Cleaning up system..."
        docker system prune -f
        
        print_status "Cleanup completed!"
    else
        print_status "Cleanup cancelled."
    fi
}

# Show help
show_help() {
    print_header "Post, Interaction & Reel Service - Docker Management"
    
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start all services"
    echo "  stop      Stop all services"
    echo "  restart   Restart all services"
    echo "  logs      Show application logs"
    echo "  status    Show service status"
    echo "  test      Run tests"
    echo "  init-db   Initialize database"
    echo "  cleanup   Clean up everything"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs"
    echo "  $0 test"
}

# Main script logic
case "$1" in
    start)
        start_all
        ;;
    stop)
        stop_all
        ;;
    restart)
        restart_all
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    test)
        run_tests
        ;;
    init-db)
        init_db
        ;;
    cleanup)
        cleanup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac



