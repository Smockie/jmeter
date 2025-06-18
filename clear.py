import subprocess

def clear_jmeter():
	subprocess.run(["rm", "-rf", "/home/jmeter/files/results.jtl", "/home/jmeter/rotation/results.jtl", "/home/jmeter/general/results.jtl"], check=True)
	subprocess.run(["rm", "-rf", "/home/jmeter/auth_tokens.csv", "/home/jmeter/jmeter.log", "/home/jmeter/user_id.csv"], check=True)
	subprocess.run(["rm", "-rf", "/tmp/nested_*"], check=True)
	subprocess.run(["rm", "-rf", "/home/jmeter/report/*"], check=True)
	print("Остаточные файлы очищены")

try:
	clear_jmeter()
except Exception as e:
	print(f"Ошибка при удалении файлов: {e}")
