ip=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
echo "Flask App URL"
echo "http://$ip:5000"
echo "Flask App URL(Python version)"
echo "http://$ip:5001"
echo "DB Admin URL"
echo "http://$ip:8080"
echo "SQLite Web URL"
echo "http://$ip:8000"
echo "Visualizer URL"
echo "http://$ip:8081"
