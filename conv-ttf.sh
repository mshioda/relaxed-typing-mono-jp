for otf in ./resources/NotoSansJP-*.otf; do
    ttf=${otf%.otf}.ttf
    if [ ! -f ${ttf} ]; then
	otf2ttf ${otf} ${ttf}
    fi
done
