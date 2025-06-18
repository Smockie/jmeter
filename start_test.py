import subprocess
import time
import threading

invite_url = input("Введите ссылку-приглашение:")
domain = invite_url.rstrip('/').split('/')[-3]
url_uniq = invite_url.rstrip('/').split('/')[-1]
token = input("Введите токен админа (вида Bearer xxx...):")

subprocess.run(["chmod", "+x", "spam_clear.sh"])

def reset_antispam():
    subprocess.run(["./spam_clear.sh"], check=True)
    print("Почистил лимиты")


def run_jmeter_scripts():
    scripts = [
        [
            "jmeter", "-n",
            "-t", "/home/jmeter/general/general.jmx",
            "-l", "/home/jmeter/general/results.jtl",
            "-e", "-o", "/home/jmeter/report/general",
            f"-Jdomain={domain}",
            f"-Jinvite_url={invite_url}",
            f"-Jurl_uniq={url_uniq}",
            "-Jcount=0"
        ],
        [
            "jmeter", "-n",
            "-t", "/home/jmeter/files/files.jmx",
            "-l", "/home/jmeter/files/results.jtl",
            "-e", "-o", "/home/jmeter/report/files",
            f"-Jdomain={domain}",
            f"-Jtoken={token}"
        ],
        [
            "jmeter", "-n",
            "-t", "/home/jmeter/rotation/rotation.jmx",
            "-l", "/home/jmeter/rotation/results.jtl",
            "-e", "-o", "/home/jmeter/report/rotation",
            f"-Jdomain={domain}",
            f"-Jinvite_url={invite_url}",
            f"-Jurl_uniq={url_uniq}",
            f"-Jadmin_token={token}"
        ]
    ]

    processes = []
    for cmd in scripts:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        processes.append(p)

    # Если хочешь дождаться окончания всех:
    for p in processes:
        for line in p.stdout:
            decoded = line.decode().strip()
            if 'Nashorn engine' not in decoded:  # фильтруем спам
                print(decoded)


def antispam_reset_loop(interval=3):
    while True:
        try:
            reset_antispam()
            time.sleep(interval)
        except Exception as e:
            print(f"Ошибка при чистке лимитов: {e}")
            break


if __name__ == "__main__":
    antispam_thread = threading.Thread(target=antispam_reset_loop, daemon=True)
    antispam_thread.start()

    run_jmeter_scripts()
