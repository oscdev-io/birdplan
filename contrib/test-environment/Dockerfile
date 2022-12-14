FROM idmslinux/rolling

RUN set -ex; \
    echo "Updating and installing..."; \
    pacman -Syu --noconfirm \
        python-tox \
        bgpq3 \
        bird \
        exabgp \
        iproute2; \
    echo "Cleaning up..."; \
    rm -f /var/cache/pacman/pkg/* /var/lib/pacman/sync/*

# Copy in our script
COPY runtest /root/

# Run our tests
CMD ["/root/runtest"]
