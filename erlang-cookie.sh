#! /bin/bash

echo $(openssl rand -base64 32) > erlang.cookie
