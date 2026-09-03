#!/usr/bin/env bash
#
# Docker host inventory — generic reconnaissance for planning a new deployment.
#
# READ-ONLY. Inspects only. Never pulls, builds, starts, stops, removes or
# modifies anything. Safe on a production host with live containers.
#
# Usage:
#   sudo bash docker-host-report.sh                 > report.txt
#   sudo bash docker-host-report.sh 8080 5432 6379  > report.txt   # also test those ports
#
# The output is written to be read by a human OR pasted to an LLM: every section
# is delimited, every table labelled, units explicit. Nothing is app-specific.
#
set -uo pipefail
export LC_ALL=C

WANTED_PORTS=("$@")
D="docker"
command -v docker >/dev/null 2>&1 || D=""

sec() { printf '\n\n########## %s ##########\n' "$*"; }
sub() { printf '\n--- %s ---\n' "$*"; }
kv()  { printf '%-26s %s\n' "$1:" "$2"; }

echo "=================================================================="
echo "DOCKER HOST INVENTORY"
echo "generated : $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "hostname  : $(hostname -f 2>/dev/null || hostname)"
echo "privilege : $([ "$(id -u)" -eq 0 ] && echo root || echo 'NON-ROOT (firewall + port owners incomplete; re-run with sudo)')"
echo "=================================================================="

sec "1. HOST"
kv "kernel"         "$(uname -srm)"
kv "distro"         "$( (. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME") || echo unknown)"
# systemd-detect-virt exits 1 when it reports "none", so capture output first.
VIRT="$(systemd-detect-virt 2>/dev/null)"; kv "virtualisation" "${VIRT:-unknown}"
kv "uptime"         "$(uptime -p 2>/dev/null | sed 's/^up //')"
kv "timezone"       "$(timedatectl show -p Timezone --value 2>/dev/null || cat /etc/timezone 2>/dev/null || echo unknown)"
kv "cpu cores"      "$(nproc 2>/dev/null)"
kv "load average"   "$(cut -d' ' -f1-3 /proc/loadavg 2>/dev/null)"
sub "memory and swap";   free -h 2>/dev/null
sub "filesystem usage";  df -hT 2>/dev/null | grep -vE 'tmpfs|devtmpfs|overlay|squashfs'
sub "inode usage";       df -i 2>/dev/null | grep -vE 'tmpfs|devtmpfs|overlay|squashfs'
sub "security modules"
kv "selinux"  "$(getenforce 2>/dev/null || echo 'not present')"
kv "apparmor" "$(aa-status --enabled 2>/dev/null && echo enabled || echo 'not enabled / not present')"

if [ -z "$D" ]; then
  sec "DOCKER NOT INSTALLED"; echo "docker not found on PATH."; exit 0
fi

sec "2. DOCKER ENGINE"
$D version 2>/dev/null | sed 's/^/  /' || echo "  cannot reach docker daemon (permission? try sudo)"
sub "compose availability"
if $D compose version >/dev/null 2>&1; then kv "compose plugin" "v$($D compose version --short 2>/dev/null)  (invoke: docker compose)"
else kv "compose plugin" "absent"; fi
if command -v docker-compose >/dev/null 2>&1; then
  CV="$(docker-compose version --short 2>/dev/null)"
  LEG=""; case "$CV" in 1.*) LEG="  [legacy v1]";; esac
  kv "compose standalone" "v${CV}  (invoke: docker-compose)${LEG}"
else kv "compose standalone" "absent"; fi
sub "daemon configuration"
kv "root dir"       "$($D info --format '{{.DockerRootDir}}' 2>/dev/null)"
kv "storage driver" "$($D info --format '{{.Driver}}' 2>/dev/null)"
kv "cgroup driver"  "$($D info --format '{{.CgroupDriver}}' 2>/dev/null)"
kv "logging driver" "$($D info --format '{{.LoggingDriver}}' 2>/dev/null)"
kv "live restore"   "$($D info --format '{{.LiveRestoreEnabled}}' 2>/dev/null)"
kv "containers"     "$($D info --format '{{.Containers}} total / {{.ContainersRunning}} running / {{.ContainersStopped}} stopped' 2>/dev/null)"
sub "/etc/docker/daemon.json"
if [ -r /etc/docker/daemon.json ]; then cat /etc/docker/daemon.json
else echo "(absent - defaults: address pool 172.17.0.0/16+, json-file logs with NO size cap)"; fi

sec "3. PORT MAP  <-- primary conflict surface"
sub "host ports published by containers"
printf '%-10s %-6s %-32s %s\n' HOSTPORT PROTO CONTAINER STATE
$D ps -a --format '{{.Names}}\t{{.Ports}}\t{{.State}}' 2>/dev/null \
| awk -F'\t' '{n=$1; st=$3; c=split($2,p,", ");
   for(i=1;i<=c;i++){ if(match(p[i],/:[0-9]+->/)){
     hp=substr(p[i],RSTART+1,RLENGTH-3); pr=(p[i]~/udp/)?"udp":"tcp";
     k=hp"|"pr"|"n; if(!(k in s)){s[k]=1; printf "%-10s %-6s %-32s %s\n",hp,pr,n,st}}}}' | sort -n
sub "ALL listening sockets (docker and non-docker)"
if [ "$(id -u)" -eq 0 ]; then ss -ltnup 2>/dev/null | awk 'NR>1{printf "%-6s %-24s %s\n",$1,$5,$7}' | sort -u
else ss -ltnu 2>/dev/null | awk 'NR>1{printf "%-6s %-24s\n",$1,$5}' | sort -u; echo "(process owners hidden - run as root)"; fi
sub "occupied ports, deduplicated"
{ $D ps -a --format '{{.Ports}}' 2>/dev/null | grep -oE ':[0-9]+->' | tr -d ':>-'
  ss -ltnu 2>/dev/null | awk 'NR>1{print $5}' | sed 's/.*://'; } | grep -E '^[0-9]+$' | sort -n -u | tr '\n' ' '; echo
if [ ${#WANTED_PORTS[@]} -gt 0 ]; then
  sub "requested port availability"
  for p in "${WANTED_PORTS[@]}"; do
    B=""
    ss -ltnu 2>/dev/null | awk -v q=":$p\$" '$5 ~ q' | grep -q . && B="host listener"
    $D ps -a --format '{{.Names}} {{.Ports}}' 2>/dev/null | grep -qE ":$p->" && B="${B:+$B, }container publish"
    printf '%-10s %s\n' "$p" "${B:-FREE}"
  done
fi

sec "4. CONTAINERS"
sub "running";  $D ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null
sub "not running"; $D ps -a --filter status=exited --filter status=created --filter status=dead \
  --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}' 2>/dev/null
sub "restart policy and health (these reclaim ports on reboot)"
printf '%-32s %-16s %-10s %s\n' NAME RESTART HEALTH IMAGE
for c in $($D ps -aq 2>/dev/null); do
  $D inspect "$c" --format '{{printf "%-32s %-16s %-10s %s" .Name .HostConfig.RestartPolicy.Name (or .State.Health.Status "-") .Config.Image}}' 2>/dev/null | sed 's|^/||'
done

sec "5. COMPOSE PROJECTS"
printf '%-24s %-26s %s\n' PROJECT SERVICE WORKING_DIR
for c in $($D ps -aq 2>/dev/null); do
  $D inspect "$c" --format '{{index .Config.Labels "com.docker.compose.project"}}|{{index .Config.Labels "com.docker.compose.service"}}|{{index .Config.Labels "com.docker.compose.project.working_dir"}}' 2>/dev/null
done | grep -vE '^\|\|?$' | sort -u | awk -F'|' 'NF>1{printf "%-24s %-26s %s\n",$1,$2,$3}'
echo
echo "NOTE: compose takes its project name from the directory it runs in. A new"
echo "      deployment needs a directory name absent above, or an explicit -p."

sec "6. NETWORKS AND ADDRESS SPACE"
printf '%-34s %-10s %-20s %s\n' NAME DRIVER SUBNET GATEWAY
for n in $($D network ls --format '{{.Name}}' 2>/dev/null); do
  $D network inspect "$n" --format '{{printf "%-34s %-10s" .Name .Driver}}{{range .IPAM.Config}}{{printf " %-20s %s" .Subnet .Gateway}}{{end}}' 2>/dev/null; echo
done
sub "containers attached per network"
for n in $($D network ls --format '{{.Name}}' 2>/dev/null); do
  M=$($D network inspect "$n" --format '{{range .Containers}}{{.Name}} {{end}}' 2>/dev/null)
  [ -n "${M// }" ] && printf '%-34s %s\n' "$n" "$M"
done
sub "address pool consumption"
echo "Default pool: 172.17.0.0/16 .. 172.31.0.0/16 (16 blocks). Each compose"
echo "project consumes at least one; exhaustion causes 'no available IPv4 pool'."
kv "172.x blocks in use" "$($D network ls --format '{{.Name}}' 2>/dev/null | while read -r n; do $D network inspect "$n" --format '{{range .IPAM.Config}}{{.Subnet}}{{end}}' 2>/dev/null; done | grep -c '^172\.')"
kv "custom pool configured" "$(grep -c 'default-address-pools' /etc/docker/daemon.json 2>/dev/null || echo 0)"

sec "7. IMAGES, VOLUMES, DISK"
sub "docker disk usage"; $D system df 2>/dev/null
sub "images by size (top 20)"; $D images --format '{{.Size}}\t{{.Repository}}:{{.Tag}}' 2>/dev/null | sort -hr | head -20
sub "dangling images"; echo "$($D images -f dangling=true -q 2>/dev/null | wc -l) dangling"
sub "named volumes"
printf '%-40s %s\n' NAME MOUNTPOINT
$D volume ls --format '{{.Name}}' 2>/dev/null | while read -r v; do
  $D volume inspect "$v" --format '{{printf "%-40s %s" .Name .Mountpoint}}' 2>/dev/null; echo; done
sub "bind mounts (host paths containers depend on)"
for c in $($D ps -aq 2>/dev/null); do
  $D inspect "$c" --format '{{$n := .Name}}{{range .Mounts}}{{if eq .Type "bind"}}{{$n}} {{.Source}} -> {{.Destination}}
{{end}}{{end}}' 2>/dev/null
done | sed 's|^/||' | grep -v '^$' | sort -u | head -30
sub "container log sizes (json-file grows unbounded by default)"
if [ "$(id -u)" -eq 0 ]; then du -ch /var/lib/docker/containers/*/*-json.log 2>/dev/null | sort -hr | head -10 || echo "(none)"
else echo "(needs root)"; fi

sec "8. FIREWALL AND EXPOSURE"
sub "ufw"; command -v ufw >/dev/null 2>&1 && { ufw status verbose 2>/dev/null || echo "(needs root)"; } || echo "not installed"
sub "firewalld"; command -v firewall-cmd >/dev/null 2>&1 && firewall-cmd --state 2>/dev/null || echo "not installed"
sub "iptables DOCKER-USER"; iptables -L DOCKER-USER -n --line-numbers 2>/dev/null || echo "(needs root, or nftables in use)"
echo
echo "IMPORTANT: docker writes its own iptables rules that BYPASS ufw. A port"
echo "           published with -p is internet-reachable even when ufw denies it."
echo "           Bind to 127.0.0.1 (e.g. 127.0.0.1:8080:80) to keep it host-local."
sub "reverse proxies / ingress"
$D ps --format '{{.Names}}\t{{.Image}}\t{{.Ports}}' 2>/dev/null | grep -Ei 'nginx|traefik|caddy|haproxy|envoy|swag|proxy' || echo "none obvious among containers"
for p in 80 443; do printf 'host port %-4s : %s\n' "$p" "$(ss -ltn 2>/dev/null | awk -v q=":$p\$" '$4 ~ q {print "OCCUPIED"; f=1} END{if(!f) print "free"}' | head -1)"; done

sec "9. NON-DOCKER SERVICES HOLDING PORTS"
command -v systemctl >/dev/null 2>&1 && \
  { systemctl list-units --type=service --state=running --no-pager --no-legend 2>/dev/null | awk '{print $1}' \
    | grep -Ei 'nginx|apache|httpd|caddy|mysql|mariadb|postgres|redis|mongo|rabbit|memcach|gunicorn|uwsgi|tomcat|node' \
    || echo "(none of the usual port-holders under systemd)"; } || echo "systemd not present"

sec "10. FACTS FOR ANALYSIS"
kv "cpu cores"            "$(nproc 2>/dev/null)"
kv "memory total"         "$(free -h 2>/dev/null | awk '/^Mem:/{print $2}')"
kv "memory available"     "$(free -h 2>/dev/null | awk '/^Mem:/{print $7}')"
kv "swap total"           "$(free -h 2>/dev/null | awk '/^Swap:/{print $2}')"
kv "root fs free"         "$(df -h / 2>/dev/null | awk 'NR==2{print $4" of "$2" ("$5" used)"}')"
kv "docker dir free"      "$(df -h "$($D info --format '{{.DockerRootDir}}' 2>/dev/null || echo /var/lib/docker)" 2>/dev/null | awk 'NR==2{print $4}')"
kv "containers running"   "$($D ps -q 2>/dev/null | wc -l)"
kv "containers total"     "$($D ps -aq 2>/dev/null | wc -l)"
kv "images"               "$($D images -q 2>/dev/null | wc -l)"
kv "networks"             "$($D network ls -q 2>/dev/null | wc -l)"
kv "volumes"              "$($D volume ls -q 2>/dev/null | wc -l)"
kv "compose projects"     "$($D ps -a --format '{{.Label "com.docker.compose.project"}}' 2>/dev/null | grep -v '^$' | sort -u | paste -sd, - | sed 's/,/, /g')"
kv "published host ports" "$($D ps -a --format '{{.Ports}}' 2>/dev/null | grep -oE ':[0-9]+->' | tr -d ':>-' | sort -n -u | paste -sd' ')"

printf '\n\n=== END OF REPORT ===\n'
