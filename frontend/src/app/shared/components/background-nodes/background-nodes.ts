import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

type Node = {
  x: number;
  y: number;
  r: number;
};

@Component({
  selector: 'app-background-nodes',
  imports: [CommonModule],
  templateUrl: './background-nodes.html',
  styleUrl: './background-nodes.scss',
})
export class BackgroundNodes {
  nodes: Node[] = [];
  links: { from: number; to: number }[] = [];

  constructor() {
    this.generateGraph();
  }

  generateGraph() {
    const count = 40;

    this.nodes = Array.from({ length: count }).map(() => ({
      x: Math.random() * 1000,
      y: Math.random() * 600,
      r: Math.random() > 0.7 ? 6 : 4
    }));

    for (let i = 0; i < count; i++) {
      for (let j = i + 1; j < count; j++) {
        if (Math.random() > 0.92) {
          this.links.push({ from: i, to: j });
        }
      }
    }
  }

  onHover(index: number) {
    const nodeEls = document.querySelectorAll<SVGCircleElement>('.ui-node');
    const lineEls = document.querySelectorAll<SVGLineElement>('.ui-node-line');

    nodeEls[index]?.classList.add('ui-node-hovered');

    lineEls.forEach((line, i) => {
      if (
        this.links[i]?.from === index ||
        this.links[i]?.to === index
      ) {
        line.classList.add('ui-node-line-active');
      }
    });
  }

  onLeave() {
    document
      .querySelectorAll('.ui-node-hovered')
      .forEach(el => el.classList.remove('ui-node-hovered'));

    document
      .querySelectorAll('.ui-node-line-active')
      .forEach(el => el.classList.remove('ui-node-line-active'));
  }
}
