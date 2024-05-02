#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2024, AllWorldIT.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# type: ignore

"""OpenSSH support functions."""

from typing import Tuple

import cryptography.hazmat.primitives
import cryptography.hazmat.primitives.asymmetric.ed25519

# import cryptography.hazmat.primitives.asymmetric.rsa
import cryptography.hazmat.primitives.serialization


def generate_openssh_keypair() -> Tuple[str, str]:
    """Generate a new OpenSSH key pair."""

    # Generate host private key
    key = cryptography.hazmat.primitives.asymmetric.ed25519.Ed25519PrivateKey.generate()
    # key = cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key(public_exponent=65537, key_size=4096)
    privpem = key.private_bytes(
        encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM,
        format=cryptography.hazmat.primitives.serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=cryptography.hazmat.primitives.serialization.NoEncryption(),
    )
    privkey = privpem.decode()

    # Generate host public key
    pub = key.public_key()
    pubkey = pub.public_bytes(
        encoding=cryptography.hazmat.primitives.serialization.Encoding.OpenSSH,
        format=cryptography.hazmat.primitives.serialization.PublicFormat.OpenSSH,
    ).decode()

    return [privkey, pubkey]
