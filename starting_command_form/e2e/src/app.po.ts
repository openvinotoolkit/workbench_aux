import { browser, by, element } from 'protractor';

export class AppPage {
  async navigateTo() {
    return browser.get('/');
  }

  async getGeneralOptionsHeader(): Promise<string> {
    return element(by.css(`[data-test-id="general-options-header"]`)).getText();
  }
}
