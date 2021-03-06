# Copyright (c) 2014 by California Institute of Technology
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the California Institute of Technology nor
#    the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CALTECH
# OR THE CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import os.path
import subprocess


def retrieve_version_from_git():
    """Returns a string.
    If the git command fails, it returns 'unknown-commit'.
    If HEAD has tag with prefix "vM" where M is an integer, it returns the tag.
    If HEAD has any other tag, it returns "dev-" plus the tag.
    """
    if os.path.exists('.git'):
        # Is Git installed?
        try:
            subprocess.call(['git', '--version'],
                            stdout=subprocess.PIPE)
        except OSError:
            return "unknown.commit"

        # Get a tag from git.
        p = subprocess.Popen(
            ['git', 'describe', '--tags', 'HEAD'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        p.wait()
        if p.returncode == 0:
            tag = p.stdout.read().decode('utf-8')
            if tag.endswith('\n'):
                tag = tag[:-1]
            if len(tag) >= 2 and tag.startswith('v'):
                # It's probably a version number
                try:
                    int(tag[1])
                except ValueError:
                    return 'dev0+' + tag
                # Get create a PEP440 compliant version number.
                if tag.find('-') < 0:
                    return tag[1:]
                else:
                    split = tag.find('-')
                    return tag[1:split] + '+dev' + tag[split+1:].replace('-','.')

        return "unknown.commit"
