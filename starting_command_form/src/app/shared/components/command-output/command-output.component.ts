import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'wb-command-output',
  templateUrl: './command-output.component.html',
  styleUrls: ['./command-output.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CommandOutputComponent {
  @Input()
  copy = false;

  constructor(private _snackBar: MatSnackBar) {}

  copyCommand({ innerText }: HTMLElement): void {
    const copyCommandPromise = navigator?.clipboard ? navigator?.clipboard?.writeText(innerText) : this.copyCommandFallback(innerText);
    copyCommandPromise.then(() => {
      this._snackBar.open('Copied', null, {
        duration: 1000,
        panelClass: 'copy-snackbar'
      });
    });
  }

  private copyCommandFallback(innerText: string): Promise<void> {
    const tempTextArea = document.createElement('textarea');
    tempTextArea.value = innerText;
    tempTextArea.style.position = 'absolute';
    tempTextArea.style.opacity = '0';
    document.body.appendChild(tempTextArea);
    tempTextArea.select();
    return new Promise<void>(((resolve, reject) => {
      document.execCommand('copy') ? resolve() : reject();
      tempTextArea.remove();
    }));
  }
}
