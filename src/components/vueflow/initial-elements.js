import {MarkerType} from '@vue-flow/core'
import { Position, VueFlow } from '@vue-flow/core'

export const initialNodes = [
    {
        id: '1',
        type: 'input',
        data: {label: 'Node 1'},
        position: {x: 250, y: 0},
        class: 'light',
    },
    {
        id: '2',
        type: 'output',
        data: {label: 'Node 2'},
        position: {x: 100, y: 100},
        class: 'light',
    },
    {
        id: '3',
        data: {label: 'Node 3'},
        position: {x: 400, y: 100},
        class: 'light',
    },
    {
        id: '4',
        data: {label: 'Node 4'},
        position: {x: 150, y: 200},
        class: 'light',
    },
    {
        id: '5',
        type: 'output',
        data: {label: 'Node 5'},
        position: {x: 300, y: 300},
        class: 'light',
    },
]

export const initialEdges = [
    {
        id: 'e1-2',
        source: '1',
        target: '2',
        animated: true,
        markerEnd: MarkerType.ArrowClosed,
    },
    {
        id: 'e1-3',
        source: '1',
        target: '3',
        label: 'edge with arrowhead',
        markerEnd: MarkerType.ArrowClosed,
    },
    {
        id: 'e4-5',
        type: 'step',
        source: '4',
        target: '5',
        label: 'Node 2',
        style: {stroke: 'orange'},
        labelBgStyle: {fill: 'orange'},
    },
    {
        id: 'e3-4',
        type: 'smoothstep',
        source: '3',
        target: '4',
        label: 'smoothstep-edge',
    },
]

export const initialNodes2 = [
    {
        id: '1',
        type: 'menu',
        data: { label: 'toolbar top', toolbarPosition: Position.Top },
        position: { x: 200, y: 0 },
    },
    {
        id: '2',
        type: 'menu',
        data: { label: 'toolbar right', toolbarPosition: Position.Right },
        position: { x: -50, y: 100 },
    },
    {
        id: '3',
        type: 'menu',
        data: { label: 'toolbar bottom', toolbarPosition: Position.Bottom },
        position: { x: 0, y: 200 },
    },
    {
        id: '4',
        type: 'menu',
        data: { label: 'toolbar left', toolbarPosition: Position.Left },
        position: { x: 200, y: 300 },
    },
    {
        id: '5',
        type: 'menu',
        data: { label: 'toolbar always open', toolbarPosition: Position.Top, toolbarVisible: true },
        position: { x: 0, y: -100 },
    },
]

const edges = [
    { id: 'e1-2', source: '1', target: '2', label: 'bezier edge (default)', class: 'normal-edge' },
    { id: 'e2-2a', source: '2', target: '2a', type: 'smoothstep', label: 'smoothstep edge' },
    { id: 'e2-3', source: '2', target: '3', type: 'step', label: 'step edge' },
    { id: 'e3-4', source: '3', target: '4', type: 'straight', label: 'straight edge' },
    { id: 'e3-3a', source: '3', target: '3a', type: 'straight', label: 'label only edge', style: { stroke: 'none' } },
    { id: 'e3-5', source: '4', target: '5', animated: true, label: 'animated styled edge', style: { stroke: '#10b981' } },
    {
        id: 'e2a-6',
        source: '2a',
        target: '6',
        label: () => h(CustomEdgeLabel, { label: 'custom label text' }),
        labelStyle: { fill: '#10b981', fontWeight: 700 },
        markerEnd: MarkerType.Arrow,
    },
    {
        id: 'e5-7',
        source: '5',
        target: '7',
        label: 'label with bg',
        labelBgPadding: [8, 4],
        labelBgBorderRadius: 4,
        labelBgStyle: { fill: '#FFCC00', color: '#fff', fillOpacity: 0.7 },
        markerEnd: MarkerType.ArrowClosed,
    },
    {
        id: 'e5-8',
        source: '5',
        target: '8',
        type: 'button',
        data: { text: 'custom edge' },
        markerEnd: MarkerType.ArrowClosed,
    },
    {
        id: 'e4-9',
        source: '4',
        target: '9',
        type: 'custom',
        data: { text: 'styled custom edge label' },
    },
]