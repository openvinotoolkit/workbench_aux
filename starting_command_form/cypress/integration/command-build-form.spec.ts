import * as data from '../../src/assets/data/messages.json';
import * as referenceCommands from '../fixtures/reference-commands.json';

import { FormControlNames, Devices } from '../../src/app/shared/models/command-constructor-form';


describe('UI tests on command build form', () => {
  it('should visit the home page and check the headers', () => {
    cy.visit('/');
    cy.contains(data.sectionHeaders.generalOptions);
    cy.contains(data.sectionHeaders.advancedOptions);
    cy.contains(data.sectionHeaders.results);
  });

  it('should visit the home page and check the initial selection and default commands', () => {
    cy.visit('/');

    // Check Docker
    cy.getNestedElementByTestID(FormControlNames.DOCKER_INSTALLED, 'true').should('have.class', 'mat-radio-checked');
    cy.getNestedElementByTestID(FormControlNames.DOCKER_INSTALLED, 'false').should('not.have.class', 'mat-radio-checked');
    // Check OS
    cy.getElementByTestID('linux').should('have.class', 'mat-radio-checked');
    cy.getElementByTestID('windows').should('not.have.class', 'mat-radio-checked');

    // Check way of starting
    cy.getElementByTestID('python').should('have.class', 'mat-radio-checked');
    cy.getElementByTestID('docker').should('not.have.class', 'mat-radio-checked');

    // Check devices
    Object.keys(Devices).forEach((device: string) => {
      if (device === Devices.CPU) {
        cy.getElementByTestID(device).should('have.class', 'mat-checkbox-checked');
      } else {
        cy.getElementByTestID(device).should('not.have.class', 'mat-checkbox-checked');
      }
    });

    // Check resulting command
    cy.getElementByTestID('resulting-command').should('have.text', referenceCommands.initialStartingCommand);
    cy.getElementByTestID('install-starter-command').should('have.text', referenceCommands.installPythonStarterCommand);
  });

  it('should select additional devices (GPU, MYRIAD) and check that command is changed accordingly', () => {
    cy.visit('/');

    // Select checkboxes
    cy.getElementByTestID('devices-warning').should('not.exist');
    cy.getElementByTestID(Devices.GPU).click().should('have.class', 'mat-checkbox-checked');
    cy.getElementByTestID(Devices.NCS2).click().should('have.class', 'mat-checkbox-checked');
    // Check that warning is present
    cy.getElementByTestID('devices-warning').should('be.visible').and('have.text', data.warnings.incompatibleDevices);
    cy.getElementByTestID('resulting-command').should('have.text', referenceCommands.startingCommandGPUMYRIAD);
    });
});
