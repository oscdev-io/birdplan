FROM idmslinux/rolling

RUN set -ex; \
    echo "Updating and installing..."; \
    pacman -Syu --noconfirm \
        python-pytest-runner \
        python-pytest-cov \
        python-pytest-black \
        python-pytest-flake8 \
        python-pytest-pycodestyle \
        python-pytest-pydocstyle \
        python-pytest-pylint \
        python-pytest-mypy \
        python-requests \
        python-yaml \
        iproute2 \
        bird \
        exabgp; \
    echo "Cleaning up..."; \
    rm -f /var/cache/pacman/pkg/* /var/lib/pacman/sync/*

# Copy in our script
COPY runtest /root/

# Run our tests
CMD ["/root/runtest"]