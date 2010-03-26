// vim: ts=4:sw=4:nu:fdc=4:nospell
/*global Ext, window, document, setTimeout */

/**
 * @class Ext.ux.ParkingFileTreePanel
 * @extends Ext.ux.FileTreePanel
 */

Ext.ux.ParkingFileTreePanel = Ext.extend(Ext.ux.FileTreePanel, {
	// {{{
	/**
	 * returns (and lazy create) the context menu
	 * @private
	 */
	getContextMenu:function() {
		// lazy create context menu
		if(!this.contextmenu) {
			var config = {
				 singleUpload:this.singleUpload
				,maxFileSize:this.maxFileSize
				,enableProgress:this.enableProgress
			};
			if(this.baseParams) {
				config.baseParams = this.baseParams;
			}
			this.contextmenu = new Ext.ux.ParkingFileTreeMenu(config);
			this.contextmenu.on({click:{scope:this, fn:this.onContextClick}});

			this.uploadPanel = this.contextmenu.getItemByCmd('upload-panel').component;
			this.uploadPanel.on({
				 beforeupload:{scope:this, fn:this.onBeforeUpload}
				,allfinished:{scope:this, fn:this.onAllFinished}
			});
			this.uploadPanel.setUrl(this.uploadUrl || this.url);
		}
		return this.contextmenu;
	} // eo function getContextMenu
	// }}}
	// {{{
	/**
	 * adjusts context menu depending on many things and shows it
	 * @private
	 * @param {Ext.tree.AsyncTreeNode} node Node on which was right-clicked
	 */
	,showContextMenu:function(node) {

		// setup node alignment
		var topAlign = false;
		var alignEl = this.topMenu ? this.topMenu.getEl() : this.body;

		if(!node) {
			node = this.getSelectionModel().getSelectedNode();
			topAlign = true;
		}
		else {
			alignEl = node.getUI().getEl();
		}
		if(!node) {
			return;
		}

		var menu = this.getContextMenu();
		menu.node = node;

		// set node name
		menu.getItemByCmd('nodename').setText(Ext.util.Format.ellipsis(node.text, 22));

		// enable/disable items depending on node clicked
		menu.setItemDisabled('open', !node.isLeaf());
		menu.setItemDisabled('reload', node.isLeaf());
		menu.setItemDisabled('expand', node.isLeaf());
		menu.setItemDisabled('collapse', node.isLeaf());
		menu.setItemDisabled('delete', node === this.root || node.disabled);
		menu.setItemDisabled('rename', this.readOnly || node === this.root || node.disabled);
		menu.setItemDisabled('newdir', this.readOnly || (node.isLeaf() ? node.parentNode.disabled : node.disabled));
		menu.setItemDisabled('upload-panel', node.isLeaf() ? node.parentNode.disabled : node.disabled);
		
		// show/hide logic
		menu.getItemByCmd('open').setVisible(this.enableOpen);
		menu.getItemByCmd('delete').setVisible(this.enableDelete);
		menu.getItemByCmd('newdir').setVisible(this.enableNewDir);
		menu.getItemByCmd('rename').setVisible(this.enableRename);
		menu.getItemByCmd('upload-panel').setVisible(this.enableUpload);
		menu.getItemByCmd('sep-collapse').setVisible(this.enableNewDir || this.enableDelete || this.enableRename);

		// select node
		node.select();

		// show menu
		if(topAlign) {
			menu.showAt(menu.getEl().getAlignToXY(alignEl, 'tl-bl?'));
		}
		else {
			menu.showAt(menu.getEl().getAlignToXY(alignEl, 'tl-tl?', [0, 18]));
		}
	} // eo function 
	// }}}
}); // eo extend

// register xtype
Ext.reg('filetreepanel', Ext.ux.FileTreePanel);

// eof
