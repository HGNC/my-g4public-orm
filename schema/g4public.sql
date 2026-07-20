/*
 Navicat MySQL Dump SQL

 Source Server         : GCP - HGNC
 Source Server Type    : MySQL
 Source Server Version : 80408 (8.4.8-google)
 Source Host           : 35.246.28.232:3306
 Source Schema         : g4public_2026_06_30

 Target Server Type    : MySQL
 Target Server Version : 80408 (8.4.8-google)
 File Encoding         : 65001

 Date: 30/06/2026 15:47:13
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cell
-- ----------------------------
DROP TABLE IF EXISTS `cell`;
CREATE TABLE `cell` (
  `cell_id` int DEFAULT NULL,
  `cell_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `cell_alias` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `cell_table` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `cell_permit` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `cell_view` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `cell_edit` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `cell_lint` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `cell_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `cell_sort` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `hgnc_id` int DEFAULT NULL,
  `note` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  KEY `comment_hgnc_id_index` (`hgnc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for external_resource
-- ----------------------------
DROP TABLE IF EXISTS `external_resource`;
CREATE TABLE `external_resource` (
  `id` int NOT NULL DEFAULT '0',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `approved` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for family_alias
-- ----------------------------
DROP TABLE IF EXISTS `family_alias`;
CREATE TABLE `family_alias` (
  `id` int DEFAULT NULL,
  `family_id` int DEFAULT NULL,
  `alias` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for family_has_external_resource
-- ----------------------------
DROP TABLE IF EXISTS `family_has_external_resource`;
CREATE TABLE `family_has_external_resource` (
  `family_id` int DEFAULT NULL,
  `ext_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for family_has_specialist
-- ----------------------------
DROP TABLE IF EXISTS `family_has_specialist`;
CREATE TABLE `family_has_specialist` (
  `fam_id` int DEFAULT NULL,
  `specialist_id` int DEFAULT NULL,
  KEY `family_has_specialist_fam_id_index` (`fam_id`),
  KEY `family_has_specialist_specialist_id_index` (`specialist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for family_new
-- ----------------------------
DROP TABLE IF EXISTS `family_new`;
CREATE TABLE `family_new` (
  `id` int NOT NULL DEFAULT '0',
  `abbreviation` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `editor` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `curator_comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `external_note` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `pubmed_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `desc_comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `desc_label` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `desc_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `desc_go` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `typical_gene` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `family_new_abbreviation_index` (`abbreviation`),
  KEY `family_new_name_index` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for gencc
-- ----------------------------
DROP TABLE IF EXISTS `gencc`;
CREATE TABLE `gencc` (
  `uuid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `hgnc_id` int DEFAULT NULL,
  `disease_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `disease_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `omim_id` int DEFAULT NULL,
  KEY `gencc_hgnc_id_index` (`hgnc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for gene_has_family
-- ----------------------------
DROP TABLE IF EXISTS `gene_has_family`;
CREATE TABLE `gene_has_family` (
  `hgnc_id` int DEFAULT NULL,
  `family_id` int DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `custom_sort` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  KEY `gene_has_family_family_id_index` (`family_id`),
  KEY `gene_has_family_hgnc_id_index` (`hgnc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for hcop_orthologs
-- ----------------------------
DROP TABLE IF EXISTS `hcop_orthologs`;
CREATE TABLE `hcop_orthologs` (
  `orth_id` int NOT NULL AUTO_INCREMENT,
  `taxon_a` int NOT NULL,
  `taxon_b` int NOT NULL,
  `db_id_a` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `db_id_b` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `vgnc_a` varchar(28) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vgnc_b` varchar(28) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ensembl_a` varchar(28) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ensembl_b` varchar(28) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `entrez_a` varchar(28) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `entrez_b` varchar(28) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `symbol_a` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `symbol_b` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `symbol_source_a` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `symbol_source_b` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name_a` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `name_b` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `source_name_a` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `source_name_b` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `locus_type_a` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `locus_type_b` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `locus_source_a` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `locus_source_b` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `class_a` enum('Gene','Approved') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `class_b` enum('Gene','Approved') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `chr_a` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `chr_b` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `support` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `text_link_a` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `text_link_b` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NOT NULL,
  PRIMARY KEY (`orth_id`) USING BTREE,
  KEY `ho_ta_tb_idx` (`taxon_a`,`taxon_b`) USING BTREE,
  KEY `ho_idataxa_idx` (`db_id_a`,`taxon_a`) USING BTREE,
  KEY `ho_idbtaxb_idx` (`db_id_b`,`taxon_b`) USING BTREE,
  KEY `ho_enstaxa_idx` (`ensembl_a`,`taxon_a`) USING BTREE,
  KEY `ho_enstaxb_idx` (`ensembl_b`,`taxon_b`) USING BTREE,
  KEY `ho_enztaxa_idx` (`entrez_a`,`taxon_a`) USING BTREE,
  KEY `ho_enztaxb_idx` (`entrez_b`,`taxon_b`) USING BTREE,
  KEY `ho_symtaxa_idx` (`symbol_a`,`taxon_a`) USING BTREE,
  KEY `ho_symtaxb_idx` (`symbol_b`,`taxon_b`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1108858376 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for hierarchy
-- ----------------------------
DROP TABLE IF EXISTS `hierarchy`;
CREATE TABLE `hierarchy` (
  `parent_fam_id` int DEFAULT NULL,
  `child_fam_id` int DEFAULT NULL,
  KEY `hierarchy_child_fam_id_index` (`child_fam_id`),
  KEY `hierarchy_parent_fam_id_index` (`parent_fam_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for hierarchy_closure
-- ----------------------------
DROP TABLE IF EXISTS `hierarchy_closure`;
CREATE TABLE `hierarchy_closure` (
  `parent_fam_id` int DEFAULT NULL,
  `child_fam_id` int DEFAULT NULL,
  `distance` int DEFAULT NULL,
  KEY `hierarchy_closure_child_fam_id_index` (`child_fam_id`),
  KEY `hierarchy_closure_parent_fam_id_index` (`parent_fam_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for locus_stats_chr
-- ----------------------------
DROP TABLE IF EXISTS `locus_stats_chr`;
CREATE TABLE `locus_stats_chr` (
  `ls_chr` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `ls_count` int DEFAULT NULL,
  `ls_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `ls_group` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `ls_source` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `ls_sort` int DEFAULT NULL,
  `ls_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for mane
-- ----------------------------
DROP TABLE IF EXISTS `mane`;
CREATE TABLE `mane` (
  `id` int NOT NULL,
  `ncbi_gene_id` int NOT NULL,
  `ensembl_gene` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `hgnc_id` int DEFAULT NULL,
  `refseq_nuc_acc` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `ensembl_nuc_acc` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `mane_status` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mane_hgnc_id_index` (`hgnc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for pub_hgnc
-- ----------------------------
DROP TABLE IF EXISTS `pub_hgnc`;
CREATE TABLE `pub_hgnc` (
  `gd_hgnc_id` int DEFAULT NULL,
  `gd_app_sym` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_app_sym_sort` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_app_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_locus_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_prev_sym` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_prev_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_aliases` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_name_aliases` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_pub_chrom_map` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_pub_chrom_map_sort` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_date2app_or_res` date DEFAULT NULL,
  `gd_date_mod` date DEFAULT NULL,
  `gd_date_name_change` date DEFAULT NULL,
  `gd_pub_acc_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_enz_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_pub_eg_id` int DEFAULT NULL,
  `gd_mgd_id` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_other_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_other_ids_list` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_pubmed_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_pub_refseq_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_gene_fam_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_gene_fam_pagename` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_date_sym_change` date DEFAULT NULL,
  `gd_record_type` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_primary_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_secondary_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_pub_hseq_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_pub_hseq_seq` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_pub_hseq_molecule` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_vega_ids` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_lsdb_links` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_pub_ensembl_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_ccds_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_locus_group` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_cust_sort` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_gene_fam_links` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `md_gdb_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `md_eg_id` int DEFAULT NULL,
  `md_mim_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `md_refseq_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `md_prot_id` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `md_ensembl_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_ambiguous` tinyint(1) DEFAULT NULL,
  `md_vega_id` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_to_review` tinyint(1) DEFAULT NULL,
  `md_rna_central_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `md_lncipedia` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `md_gtrnadb` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `gd_stable_symbol` tinyint(1) DEFAULT NULL,
  `md_ucsc_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `md_rgd_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `md_mgd_id` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `gd_coord` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `md_agr` int DEFAULT NULL,
  `md_alphafold` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  KEY `pub_hgnc_gd_app_sym_index` (`gd_app_sym`),
  KEY `pub_hgnc_gd_hgnc_id_index` (`gd_hgnc_id`),
  KEY `pub_hgnc_gd_pub_eg_id_index` (`gd_pub_eg_id`),
  KEY `pub_hgnc_gd_pub_ensembl_id_index` (`gd_pub_ensembl_id`),
  KEY `pub_hgnc_md_eg_id_index` (`md_eg_id`),
  KEY `pub_hgnc_md_ensembl_id_index` (`md_ensembl_id`),
  KEY `pub_hgnc_md_vega_id_index` (`md_vega_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for rat_mus_symbol
-- ----------------------------
DROP TABLE IF EXISTS `rat_mus_symbol`;
CREATE TABLE `rat_mus_symbol` (
  `rms_id` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `rms_sym` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `rms_hgnc_id` int DEFAULT NULL,
  KEY `rat_mus_symbol_rms_id_index` (`rms_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for specialist
-- ----------------------------
DROP TABLE IF EXISTS `specialist`;
CREATE TABLE `specialist` (
  `id` int NOT NULL DEFAULT '0',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

SET FOREIGN_KEY_CHECKS = 1;
