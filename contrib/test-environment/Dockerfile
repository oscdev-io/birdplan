FROM idmslinux/rolling

RUN set -ex; \
    echo "Updating and installing..."; \
    pacman -Syu --noconfirm \
        bgpq3 \
#        python-colorama \
#        python-jinja \
#        python-pytest-runner \
#        python-pytest-cov \
#        python-pytest-black \
#        python-pytest-flake8 \
#        python-pytest-pycodestyle \
#        python-pytest-pydocstyle \
#        python-pytest-pylint \
#        python-pytest-mypy \
#        python-pytest-xdist \
#        python-requests \
#        python-yaml \
        python-tox \
        bird \
        exabgp \
        iproute2; \
    echo "Cleaning up..."; \
    rm -f /var/cache/pacman/pkg/* /var/lib/pacman/sync/*

# Copy in our script
COPY runtest /root/

# Run our tests
CMD ["/root/runtest"]
