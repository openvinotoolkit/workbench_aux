import { OperatingSystems } from './command-constructor-form';

export class OSDetector {
  private static readonly platforms = {
    windows: ['Win32', 'Win64', 'Windows', 'WinCE'],
    macOS: ['Macintosh', 'MacIntel', 'MacPPC', 'Mac68K'],
  };
  private static readonly platformRegexps = {
    windows: /Win/,
    macOS: /Mac/,
  };
  static get os(): OperatingSystems {
    const { platform } = window.navigator;
    if (OSDetector.platforms.windows.includes(platform) || OSDetector.platformRegexps.windows.test(platform)) {
      return OperatingSystems.WINDOWS;
    }
    if (OSDetector.platforms.macOS.includes(platform) || OSDetector.platformRegexps.macOS.test(platform)) {
      return OperatingSystems.MAC_OS;
    }
    return OperatingSystems.LINUX;
  }
}
