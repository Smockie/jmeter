#!/bin/bash

sudo docker exec -it $(sudo docker ps | grep php_monolith | awk '{print $1}') bash -c "mysql --skip-ssl -h\$(php -r 'echo (require \"/config/1_company.php\")[\"mysql\"][\"host\"];') -P\$(php -r 'echo (require \"/config/1_company.php\")[\"mysql\"][\"port\"];') -u\$(php -r 'echo (require \"/config/1_company.php\")[\"mysql\"][\"user\"];') -p\$(php -r 'echo (require \"/config/1_company.php\")[\"mysql\"][\"pass\"];') <<EOF
DELETE FROM company_system.antispam_ip WHERE true;
DELETE FROM company_system.antispam_user WHERE true;
DELETE FROM company_system.antispam_phone WHERE true;
EOF"