class RPLidarDirectParser:

    def __init__(self):
        self.buffer = bytearray()
        self.descriptor_found = False

    def feed_byte(self, new_bytes: bytes) -> dict | None:
        """Feed new serial bytes.

        Returns a single point dict immediately if ready, or None.
        """
        self.buffer.extend(new_bytes)

        # 1. Skip past the 7-byte start descriptor if present
        if not self.descriptor_found:
            if len(self.buffer) >= 7:
                if self.buffer[0] == 0xA5 and self.buffer[1] == 0x5A:
                    self.descriptor_found = True
                    del self.buffer[:7]
                else:
                    del self.buffer[0]
            return None

        # 2. Check if we have at least 5 bytes for ONE point
        if len(self.buffer) < 5:
            return None

        b0 = self.buffer[0]
        b1 = self.buffer[1]

        # Verify sync bits and check bit C
        s = b0 & 0x01
        inv_s = (b0 >> 1) & 0x01
        check_bit = b1 & 0x01

        if (s ^ inv_s == 1) and (check_bit == 1):
            quality = b0 >> 2
            angle_q6 = (self.buffer[2] << 7) | (b1 >> 1)
            dist_q2 = (self.buffer[4] << 8) | self.buffer[3]

            # Drop the 5 bytes from buffer immediately
            del self.buffer[:5]

            # Return the single point directly
            return {
                "start_of_scan": bool(s),
                "quality": quality,
                "angle_deg": angle_q6 / 64.0,
                "distance_mm": dist_q2 / 4.0,
            }
        else:
            # Out of sync, slide forward 1 byte and try next time
            del self.buffer[0]
            return None