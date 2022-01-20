'use babel';

import MazeSolverView from './maze-solver-view';
import { CompositeDisposable } from 'atom';

export default {

  mazeSolverView: null,
  modalPanel: null,
  subscriptions: null,

  activate(state) {
    this.mazeSolverView = new MazeSolverView(state.mazeSolverViewState);
    this.modalPanel = atom.workspace.addModalPanel({
      item: this.mazeSolverView.getElement(),
      visible: false
    });

    // Events subscribed to in atom's system can be easily cleaned up with a CompositeDisposable
    this.subscriptions = new CompositeDisposable();

    // Register command that toggles this view
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'maze-solver:toggle': () => this.toggle()
    }));
  },

  deactivate() {
    this.modalPanel.destroy();
    this.subscriptions.dispose();
    this.mazeSolverView.destroy();
  },

  serialize() {
    return {
      mazeSolverViewState: this.mazeSolverView.serialize()
    };
  },

  toggle() {
    console.log('MazeSolver was toggled!');
    return (
      this.modalPanel.isVisible() ?
      this.modalPanel.hide() :
      this.modalPanel.show()
    );
  }

};
