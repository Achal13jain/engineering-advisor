---
tags: [planning, mobile]
expected_outcome: "Store release channel: CI builds with protected signing keys, beta tracks and staged rollouts, older-device testing and crash reporting by version, remote switches, minimum supported version and a compatible API, version-tied release branches only."
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

We have a React Native app for iOS and Android with about 20k monthly users that talks to our own API. We release whenever, by building on one developer's laptop and uploading to the stores. The last release crashed on older Android phones, and it took four days to get a fix approved. How should our workflow look?
