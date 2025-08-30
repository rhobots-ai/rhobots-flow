/**
 * Type declarations for @novnc/novnc
 * Since the library doesn't provide proper TypeScript declarations,
 * we define minimal types for our usage.
 */

declare module '@novnc/novnc/core/rfb' {
  interface RFBOptions {
    scaleViewport?: boolean;
    resizeSession?: boolean;
    showDotCursor?: boolean;
    background?: string;
  }

  class RFB {
    constructor(canvas: HTMLElement, url: string, options?: RFBOptions);
    addEventListener(event: string, callback: (e?: any) => void): void;
    disconnect(): void;
  }

  export default RFB;
}
