# Message Envelope and Payload Design

## 1. Purpose

This document defines the relationship between the **message envelope** and the **message payload** for the observatory Instrument Control System (ICS) messaging protocol.

The goal is to keep messages structured, traceable, and easy to parse while avoiding unnecessary duplication between routing metadata and command/status content.

---

## 2. Design Principle

A message is divided into two parts:

```text
message envelope = protocol metadata
message payload  = command, status, telemetry, or result content
```

The envelope answers:

```text
Who sent this?
Who should receive it?
What kind of message is this?
What command, keyword, topic, or resource is this about?
How should this message be delivered?
How do we correlate it with other messages?
```

The payload answers:

```text
What value, command parameters, result, status, or error is being reported?
```

The payload should not duplicate fields that already exist in the envelope unless the message contains a batch, wildcard, compound response, or delegated/proxy response.

---

## 3. Message Envelope

Every protocol message shall use a common envelope.

### 3.1 Envelope Fields

| Field | Type | Required | Meaning |
|---|---:|---:|---|
| `version` | integer | yes | Protocol/envelope version. |
| `msg_type` | string | yes | Message type, such as `REQ`, `RESP`, `PUB`, `ACK`, or `ERROR`. |
| `trans_id` | string | yes | Transaction ID used to correlate requests, acknowledgements, responses, events, and logs. |
| `key` | string | yes | Semantic key identifying the command, keyword, telemetry topic, status topic, or resource. |
| `src_id` | string | yes | Identity of the sending node. |
| `dest_id` | string or null | no | Identity of the receiving node; null for broadcast or publish/subscribe messages. |
| `timestamp` | number | yes | Unix epoch timestamp for when the message was created. |
| `qos` | integer | no | Delivery expectation. Example: `0` best effort, `1` at least once, `2` ordered/strict. |
| `delivery_policy` | string | no | Human-readable delivery policy, such as `at-most-once` or `at-least-once`. |
| `payload` | object | yes | Message-specific content. |
| `binary` | object or null | no | Optional binary data reference or attachment metadata. |

---

## 4. Message Types

| Type | Meaning |
|---|---|
| `REQ` | Request a command, read, write, or query. |
| `ACK` | Acknowledge that a request was received and accepted for processing. |
| `RESP` | Final successful response to a request. |
| `ERROR` | Rejection or failure response. |
| `PUB` | Publish status, telemetry, event, or progress information. |
| `SUB` | Subscribe to a topic or key, if supported by the transport/profile. |
| `HELLO` | Node introduction or handshake. |
| `HEARTBEAT` | Periodic liveness message. |
| `CONFIG` | Configuration exchange or update. |

---

## 5. Envelope vs. Payload

The envelope should contain routing, identity, correlation, and protocol metadata.

The payload should contain only the value, command parameters, result, status, or error content.

---

## 6. Standard Single-Value Payload
TODO

---

## 8. Batch or Compound Payloads

TODO

---

## 9. Command Request Payload

TODO

### 9.1 Keyword Request Example

TODO

---

## 10. Command ACK Payload

For long-running commands, a daemon may send an `ACK` quickly after accepting the command.

The `ACK` means:

```text
I received the command, validated it, and accepted responsibility for executing it.
```

Example TODO

Full message TODO

---

## 11. Command Response Payload

For most commands, the final `RESP` is the command completion result.

Example TODO

---

## 12. Command Failure Payload

Rejected or failed commands should use `msg_type: ERROR` and the standard payload shape.

Example rejected command TODO


Example failed command after acceptance TODO


---

## 13. Progress / Status Event Payload

For long-running commands, daemons may publish progress or status events using `msg_type: PUB` and the same `trans_id` as the original command.

Example TODO

Progress events are informational. They do not replace the final `RESP` or `ERROR`.

---

## 14. Daemon Status Payload

Daemon status messages may be compound values.

Example TODO

---

## 15. Cancel Command Payload

Cancellation shall use the normal command envelope. The cancel request gets its own `trans_id` and references the command being cancelled.

Example TODO

---

## 16. Naming Rules

Recommended naming pattern for `key`:

```text
<domain>.<subsystem>.<resource-or-command>
```

Examples:

```text
instrument.focus.position
instrument.focus.move
instrument.camera.expose
instrument.camera.status
instrument.slit.width
instrument.slit.move
sequencer.sequence.progress
daemon.health
observatory.weather.status
```

Guidelines:

- Use stable names.
- Prefer lowercase names.
- Use dot-separated hierarchy.
- Avoid transport-specific names.
- Keep command keys and telemetry keys distinct where useful.
- Do not put routing information in the key if `src_id` and `dest_id` already provide it.

---

## 17. Summary Rules

1. The envelope carries protocol metadata.
2. The payload carries value, command, status, result, or error content.
3. Use `ACK` only when a command is accepted but not yet complete.
4. Use `RESP` for the final successful result.
5. Use `ERROR` for rejected or failed commands.
