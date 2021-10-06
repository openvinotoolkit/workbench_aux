import * as data from '../../src/assets/data/messages.json';
import * as referenceCommands from '../fixtures/reference-commands.json';

import { FormControlNames, Devices, StartTypes } from '../../src/app/shared/models/command-constructor-form';


describe('UI tests on command build form', () => {
  it('should visit the home page and check the headers', () => {
    cy.visit('/');
    cy.contains(data.sectionHeaders.generalOptions).should('exist');
    cy.contains(data.sectionHeaders.advancedOptions).should('exist');
    cy.contains(data.sectionHeaders.results).should('exist');
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
    cy.getElementByTestID(StartTypes.PYTHON).should('have.class', 'mat-radio-checked');
    cy.getElementByTestID(StartTypes.DOCKER).should('not.have.class', 'mat-radio-checked');

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

  it('should select additional devices (GPU, MYRIAD), add proxy and check that command is changed accordingly', () => {
    cy.visit('/');

    // Select checkboxes
    cy.getElementByTestID('devices-warning').should('not.exist');
    cy.getElementByTestID(Devices.GPU).click().should('have.class', 'mat-checkbox-checked');
    cy.getElementByTestID(Devices.NCS2).click().should('have.class', 'mat-checkbox-checked');
    // Check that warning is present
    cy.getElementByTestID('devices-warning').should('be.visible').and('have.text', data.warnings.incompatibleDevices);
    cy.getElementByTestID('resulting-command').should('have.text', referenceCommands.startingCommandGPUMYRIAD);

    // Check that no HDDL message is displayed
    cy.getElementByTestID('hddl-daemon-command').should('not.exist');

    // Add proxy to the command
    cy.getNestedElementByTestID(FormControlNames.HTTPS_PROXY, 'true').click();
    cy.getNestedElementByTestID(FormControlNames.HTTPS_PROXY, 'edit').click();
    cy.getNestedElementByTestID(FormControlNames.HTTPS_PROXY, 'text-input').type(referenceCommands.proxyExample);
    cy.getNestedElementByTestID(FormControlNames.HTTPS_PROXY, 'sae').click();
    cy.getElementByTestID('resulting-command').should('have.text', referenceCommands.startingCommandGPUMYRIADPROXY);
  });

  it('should select Windows, check that other than CPU devices are not selectable, check the same for MacOS', () => {
    cy.visit('/');

    cy.getElementByTestID('windows').click().should('have.class', 'mat-radio-checked');
    // Check that checkboxes are unavailable
    cy.getElementByTestID(Devices.GPU).should('have.class', 'mat-checkbox-disabled');
    cy.getElementByTestID(Devices.NCS2).should('have.class', 'mat-checkbox-disabled');
    cy.getElementByTestID(Devices.HDDL).should('have.class', 'mat-checkbox-disabled');

    cy.getElementByTestID('macos').click().should('have.class', 'mat-radio-checked');
    // Check that checkboxes are still unavailable
    cy.getElementByTestID(Devices.GPU).should('have.class', 'mat-checkbox-disabled');
    cy.getElementByTestID(Devices.NCS2).should('have.class', 'mat-checkbox-disabled');
    cy.getElementByTestID(Devices.HDDL).should('have.class', 'mat-checkbox-disabled');

    cy.getElementByTestID('windows').should('not.have.class', 'mat-radio-checked');
  });

  it('should select Docker as start option, check that command is modified', () => {
    cy.visit('/');

    cy.getElementByTestID(StartTypes.DOCKER).click().should('have.class', 'mat-radio-checked');
    // Check that there is pull command
    cy.getElementByTestID('pull-image-command').should('have.text', referenceCommands.pullImageCommand);
    // Check that there is start command
    cy.getElementByTestID('resulting-command').should('have.text', referenceCommands.startingCommandDocker);

    // Select additional devices, check that the command has been changed each time
    cy.getElementByTestID(Devices.GPU).click();
    cy.getElementByTestID('resulting-command').should('have.text', referenceCommands.startingCommandDockerGPU);

    cy.getElementByTestID(Devices.NCS2).click();
    cy.getElementByTestID('resulting-command').should('have.text', referenceCommands.startingCommandDockerGPUMYRIAD);

    // Uncheck MYRIAD and select HDDL instead
    cy.getElementByTestID(Devices.NCS2).click();
    cy.getElementByTestID('hddl-daemon-command').should('not.exist');
    cy.getElementByTestID(Devices.HDDL).click();
    cy.getElementByTestID('resulting-command').should('have.text', referenceCommands.startingCommandDockerGPUHDDL);
    cy.getElementByTestID('hddl-daemon-command').should('exist').and('have.text', referenceCommands.hddlDaemonStartCommand);

    // Select Windows and check that the command is default - no other than CPU devices
    cy.getElementByTestID('windows').click();
    cy.getElementByTestID('resulting-command').should('have.text', referenceCommands.startingCommandDocker);

    // Add proxy to the command
    cy.getNestedElementByTestID(FormControlNames.HTTP_PROXY, 'true').click();
    cy.getNestedElementByTestID(FormControlNames.HTTP_PROXY, 'edit').click();
    cy.getNestedElementByTestID(FormControlNames.HTTP_PROXY, 'text-input').type(referenceCommands.proxyExample);
    cy.getNestedElementByTestID(FormControlNames.HTTP_PROXY, 'save').click();
    cy.getElementByTestID('resulting-command').should('have.text', referenceCommands.startingCommandDockerWithProxy);
  });
});
