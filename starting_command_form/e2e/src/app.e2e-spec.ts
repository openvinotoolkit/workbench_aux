import { AppPage } from './app.po';

describe('E2E tests on the command builder', () => {
  let page: AppPage;

  beforeEach(() => {
    page = new AppPage();
  });

  it('should display options header', async () => {
    await page.navigateTo();
    expect(await page.getGeneralOptionsHeader()).toEqual('General Options');
  });
});
